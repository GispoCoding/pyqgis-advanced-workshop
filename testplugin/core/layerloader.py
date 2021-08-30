import logging
from typing import Optional

from qgis.core import QgsMapLayer, QgsProject, QgsRasterLayer, QgsVectorLayer

from testplugin.definitions.file_extensions import RASTER_EXTENSIONS, VECTOR_EXTENSIONS
from testplugin.qgis_plugin_tools.tools.resources import plugin_name

LOGGER = logging.getLogger(plugin_name())


class LayerLoader:
    default_vector_provider = "ogr"
    default_raster_provider = "gdal"
    wfs_provider = "wfs"
    wms_provider = "wms"

    def __init__(self, add_to_map: bool) -> None:
        self._add_to_map = add_to_map

    def _add_layer_to_project(self, layer: QgsMapLayer) -> bool:
        qgis_project = QgsProject.instance()
        LOGGER.debug(f"Adding layer: {layer.name()}")
        qgis_project.addMapLayer(layer, self._add_to_map)
        return True

    def load_layer(self, layer_name: str, file_path: str) -> bool:
        for file_suffix in VECTOR_EXTENSIONS:
            if file_suffix in file_path.lower():
                return self.load_vector_layer(layer_name, file_path)

        for file_suffix in RASTER_EXTENSIONS:
            if file_suffix in file_path.lower():
                return self.load_raster_layer(layer_name, file_path)
        return False

    def load_vector_layer(
        self, layer_name: str, file_path: str, provider: Optional[str] = None
    ) -> bool:
        provider = (
            provider if provider is not None else LayerLoader.default_vector_provider
        )
        layer = QgsVectorLayer(file_path, layer_name, provider)
        if layer.isValid():
            return self._add_layer_to_project(layer)
        else:
            LOGGER.error(f"Layer {layer_name} is not valid. Path: {file_path}")
            return False

    def load_raster_layer(
        self, layer_name: str, file_path: str, provider: Optional[str] = None
    ) -> bool:
        provider = (
            provider if provider is not None else LayerLoader.default_raster_provider
        )
        layer = QgsRasterLayer(file_path, layer_name, provider)
        if layer.isValid():
            return self._add_layer_to_project(layer)
        else:
            LOGGER.error(f"Layer {layer_name} is not valid. Path: {file_path}")
            return False

    def load_wfs_layer(self, layer_name: str, url: str) -> bool:
        return self.load_vector_layer(layer_name, url, LayerLoader.wfs_provider)

    def load_wms_layer(self, layer_name: str, url: str) -> bool:
        return self.load_raster_layer(layer_name, url, LayerLoader.wms_provider)

    def load_wmts_layer(self, layer_name: str, url: str) -> bool:
        return self.load_raster_layer(layer_name, url, LayerLoader.wms_provider)
