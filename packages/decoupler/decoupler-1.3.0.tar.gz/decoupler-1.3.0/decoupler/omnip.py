"""
Utility functions to query OmniPath.
Functions to retrieve resources from the meta-database OmniPath.
"""

import numpy as np


def check_if_omnipath():
    try:
        import omnipath as op
    except Exception:
        raise ImportError('omnipath is not installed. Please install it with: pip install omnipath')
    return op


def get_progeny(organism='human', top=100):
    """
    Pathway RespOnsive GENes for activity inference (PROGENy).

    Wrapper to access PROGENy model gene weights. Each pathway is defined with a collection of target genes, each interaction
    has an associated p-value and weight. The top significant interactions per pathway are returned.

    Parameters
    ----------
    organism : str
        Which organism to use. Only human and mouse are available.
    top : int
        Number of genes per pathway to return.

    Returns
    -------
    p : DataFrame
        Dataframe in long format containing target genes for each pathway with their associated weights and p-values.
    """

    organism = organism.lower()
    if organism not in ['human', 'mouse']:
        raise ValueError('organism can only be human or mouse.')

    op = check_if_omnipath()

    p = op.requests.Annotations.get(resources='PROGENy')
    p = p.set_index(['record_id', 'uniprot', 'genesymbol', 'entity_type', 'source', 'label'])
    p = p.unstack('label').droplevel(axis=1, level=0)
    p.columns = np.array(p.columns)
    p = p.reset_index()
    p.columns.name = None
    p = p[['genesymbol', 'p_value', 'pathway', 'weight']]
    p = p[~p.duplicated(['pathway', 'genesymbol'])]
    p['p_value'] = p['p_value'].astype(np.float32)
    p['weight'] = p['weight'].astype(np.float32)
    p = p.sort_values('p_value').groupby('pathway').head(top).sort_values(['pathway', 'p_value']).reset_index()
    p = p[['pathway', 'genesymbol', 'weight', 'p_value']]
    p['weight'] = p['weight'].astype(np.float32)
    p['p_value'] = p['p_value'].astype(np.float32)
    p.columns = ['source', 'target', 'weight', 'p_value']

    if organism == 'mouse':
        p = translate_net(p, source_tax_id=9606, target_tax_id=10090, id_type='genesymbol', translate_source=False)

    return p


def get_resource(name):
    """
    Wrapper to access resources inside Omnipath.

    This wrapper allows to easly query different prior knowledge resources. To check available resources run
    `decoupler.show_resources()`. For more information visit the official website for [Omnipath](https://omnipathdb.org/).

    Parameters
    ----------
    name : str
        Name of the resource to query.

    Returns
    -------
    df : DataFrame
        Dataframe in long format relating genes to biological entities.
    """

    resources = show_resources()
    msg = '{0} is not a valid resource. Please, run decoupler.show_resources to see the list of available resources.'
    assert name in resources, msg.format(name)

    op = check_if_omnipath()

    df = op.requests.Annotations.get(resources=name, entity_type="protein")
    df = df.set_index(['record_id', 'uniprot', 'genesymbol', 'entity_type', 'source', 'label'])
    df = df.unstack('label').droplevel(axis=1, level=0)
    df = df.drop(columns=[name for name in df.index.names if name in df.columns])
    df.columns = list(df.columns)
    df = df.reset_index()
    df = df.drop(columns=['record_id', 'uniprot', 'entity_type', 'source'])
    return df


def show_resources():
    """
    Shows available resources in Omnipath. For more information visit the official website for
    [Omnipath](https://omnipathdb.org/).

    Returns
    -------
    lst : list
        List of available resources to query with `dc.get_resource`.
    """

    op = check_if_omnipath()

    return list(op.requests.Annotations.resources())


def get_dorothea(organism='human', levels=['A', 'B', 'C'], weight_dict={'A': 1, 'B': 2, 'C': 3, 'D': 4}):
    """
    DoRothEA gene regulatory network.

    Wrapper to access DoRothEA gene regulatory network. DoRothEA is a comprehensive resource containing a curated collection of
    transcription factors (TFs) and their target genes. Each interaction is weighted by its mode of regulation (either positive
    or negative) and by its confidence level.

    Parameters
    ----------
    organism : str
        Which organism to use. Only human and mouse are available.
    levels : list
        List of confidence levels to return. Goes from A to D, A being the most confident and D being the less.
    weight_dict : dict
        Dictionary of values to divide the mode of regulation (-1 or 1), one for each confidence level. Bigger values will
        generate weights close to zero.

    Returns
    -------
    do : DataFrame
        Dataframe in long format containing target genes for each TF with their associated weights and confidence level.
    """

    organism = organism.lower()
    if organism not in ['human', 'mouse']:
        raise ValueError('organism can only be human or mouse.')

    op = check_if_omnipath()

    # Load Dorothea
    do = op.interactions.Dorothea.get(
        fields=['dorothea_level', 'extra_attrs'],
        dorothea_levels=['A', 'B', 'C', 'D'],
        genesymbols=True,
        organism=organism
    )

    # Filter extra columns
    do = do[['source_genesymbol', 'target_genesymbol', 'is_stimulation', 'is_inhibition',
             'consensus_direction', 'consensus_stimulation', 'consensus_inhibition',
             'dorothea_level']]

    # Remove duplicates
    do = do[~do.duplicated(['source_genesymbol', 'dorothea_level', 'target_genesymbol'])]

    # Assign top level if more than 2
    do['dorothea_level'] = [lvl.split(';')[0] for lvl in do['dorothea_level']]

    # Assign mode of regulation
    mor = []
    for i in do.itertuples():
        if i.is_stimulation and i.is_inhibition:
            if i.consensus_stimulation:
                mor.append(1)
            else:
                mor.append(-1)
        elif i.is_stimulation:
            mor.append(1)
        elif i.is_inhibition:
            mor.append(-1)
        else:
            mor.append(1)
    do['mor'] = mor

    # Compute weight based on confidence: mor/confidence
    do['weight'] = [(i.mor)/weight_dict[i.dorothea_level] for i in do.itertuples()]

    # Filter and rename
    do = do[['source_genesymbol', 'dorothea_level', 'target_genesymbol', 'weight']]
    do.columns = ['source', 'confidence', 'target', 'weight']

    # Filter by levels
    do = do[np.isin(do['confidence'], levels)].sort_values('confidence').reset_index(drop=True)

    if organism == 'mouse':
        do['target'] = [t.lower().capitalize() for t in do['target']]

    return do


def translate_net(
        net,
        source='source',
        target='target',
        source_tax_id=9606,
        target_tax_id=10090,
        id_type='genesymbol',
        translate_source=False,
    ):
    """
    Translate networks between species by orthology.
    
    This function downloads orthology databases from omnipath and converts genes between species. The first time you
    run this function will take a while (~15 minutes) but then it stores all the information in cache for quick
    reusability.
    
    In case you need to restart the cache, you can do it by doing: ``rm -r .pypath/cache/``

    Parameters
    ----------
    net : DataFrame
        Network in long format.
    source : str
        Column name in net with source nodes.
    target : str
        Column name in net with target nodes.
    source_tax_id : int
        NCBI Taxonomy ID of the source organism.
    target_tax_id : int
        NCBI Taxonomy ID of the target organism.
    id_type: str
        Identifier type of the source and target columns. Can be "genesymbol", "uniprot", "ensmbl"
    translate_source : bool
        Whether to also translate the source column in net.

    Returns
    -------
    hom_net : DataFrame
        Network in long format with translated genes.
    """

    # Check if pypath is installed
    try:
        from pypath.utils import homology
    except Exception:
        raise ImportError(
            'pypath-omnipath is not installed. Please install it with: '
            'pip install git+https://github.com/saezlab/pypath.git'
        )

    # Make a copy of net
    hom_net = net.copy()

    # Check if also translate source
    if translate_source:
        cols = {
            source: id_type,
            target: id_type,
        }
    else:
        cols = {
            target: id_type,
        }

    # Translate
    hom_net = homology.translate_df(
        df = hom_net,
        target = target_tax_id,
        cols = cols,
        source = source_tax_id,
    )

    # Remove duplicated based on source and target
    hom_net = hom_net[~hom_net.duplicated([source, target])]

    return hom_net
