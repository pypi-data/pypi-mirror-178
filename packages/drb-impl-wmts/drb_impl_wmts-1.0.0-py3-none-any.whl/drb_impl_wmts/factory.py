from drb import DrbNode
from drb.factory import DrbFactory
from drb_impl_http import DrbHttpNode
from drb.exceptions import DrbFactoryException

from .wmts_nodes import WmtsServiceNode


class WmtsFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbHttpNode):
            node_wmts_service = WmtsServiceNode(
                url=node.path.original_path,
                auth=node.auth)
        else:
            node_wmts_service = WmtsServiceNode(node.path.name)
        try:
            node_wmts_service.children
        except e:
            final_url = node.path.name.replace('+wmts', '')
            raise DrbFactoryException(f'Unsupported Wmts service: {final_url}')
        return node_wmts_service
