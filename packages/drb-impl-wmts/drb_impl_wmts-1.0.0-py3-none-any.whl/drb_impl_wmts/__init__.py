from . import _version
from .wmts_nodes import WmtsServiceNode, WmtsNodeOperationGetTile, \
    WmtsNodeOperationGetFeatureInfo, WmtsGetTilePredicate, \
    WmtsGetFeatureInfoPredicate

__version__ = _version.get_versions()['version']
__all__ = [
    'WmtsServiceNode',
    'WmtsNodeOperationGetTile',
    'WmtsNodeOperationGetFeatureInfo',
    'WmtsGetTilePredicate',
    'WmtsGetFeatureInfoPredicate']
