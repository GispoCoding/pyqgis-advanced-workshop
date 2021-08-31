from typing import Any, List

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsJsonUtils,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.core.additions.edit import edit

from testplugin.core.exceptions import LayerCreatorException
from testplugin.qgis_plugin_tools.tools.custom_logging import bar_msg
from testplugin.qgis_plugin_tools.tools.i18n import tr
from testplugin.qgis_plugin_tools.tools.layers import LayerType


class LayerCreator:
    segments = 10

    def __init__(self, src_srs: str, target_srs: str) -> None:
        self._src_srs = src_srs
        self._target_srs = target_srs
        self._transform = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(src_srs),
            QgsCoordinateReferenceSystem(target_srs),
            QgsProject.instance(),
        )

    def layer_from_geojson(self, layer_name: str, geojson: str) -> QgsVectorLayer:
        fields = QgsJsonUtils.stringToFields(geojson)
        features = QgsJsonUtils.stringToFeatureList(geojson, fields)
        if features:
            for l_type in LayerType:
                if (
                    QgsWkbTypes.flatType(features[0].geometry().wkbType())
                    in l_type.wkb_types
                ):
                    layer_type = l_type
                    break
        else:
            raise LayerCreatorException(
                tr("There are no features in the text provided"),
                bar_msg=bar_msg(
                    tr(
                        "Please check if the text is valid GeoJSON "
                        "and contains features"
                    )
                ),
            )

        layer = QgsVectorLayer(self._get_type_name(layer_type), layer_name, "memory")
        with edit(layer):
            for field in fields:
                succeeded = layer.addAttribute(field)
                if not succeeded:
                    raise LayerCreatorException(
                        tr(
                            "Could not add features from geojson to to layer {}",
                            layer_name,
                        )
                    )

            succeeded = layer.addFeatures(features)
            if not succeeded:
                raise LayerCreatorException(
                    tr("Could not add features from geojson to to layer {}", layer_name)
                )
        return layer

    def layer_from_wkt(
        self,
        layer_name: str,
        layer_type: LayerType,
        wkt_geometries: List[str],
        buffer: float,
    ) -> QgsVectorLayer:
        geom_type = self._get_type_name(layer_type)

        if buffer != 0.0:
            geom_type = self._get_type_name(LayerType.Polygon)
        layer = QgsVectorLayer(
            f"{geom_type}?crs={self._target_srs}", layer_name, "memory"
        )
        with edit(layer):
            for wkt_geom in wkt_geometries:
                feature = self.feature_from_wkt(wkt_geom, [], buffer)
                succeeded = layer.addFeature(feature)
                if not succeeded:
                    raise LayerCreatorException(
                        f"Could not add feature {feature.id()} to layer {layer_name}"
                    )
        return layer

    def feature_from_wkt(
        self, wkt_geom: str, attributes: List[Any], buffer: float
    ) -> QgsFeature:
        geometry = QgsGeometry.fromWkt(wkt_geom)
        result_code = geometry.transform(self._transform)
        if buffer != 0.0:
            geometry = geometry.buffer(buffer, LayerCreator.segments)
        if result_code == geometry.Success:
            feature = QgsFeature()
            feature.setAttributes(attributes)
            feature.setGeometry(geometry)
            if not feature.isValid():
                raise LayerCreatorException(
                    "Feature is not valid",
                    bar_msg=bar_msg(
                        f"Geom: {geometry.asWkt(4)}. Attributes: {attributes}"
                    ),
                )
        else:
            raise LayerCreatorException(
                "Could not transform geometry", bar_msg=bar_msg(geometry.asWkt(4))
            )
        return feature

    @staticmethod
    def _get_type_name(layer_type: LayerType) -> str:
        if layer_type == LayerType.Point:
            geom_type = "Point"
        elif layer_type == LayerType.Line:
            geom_type = "LineString"
        else:
            geom_type = "Polygon"
        return geom_type
