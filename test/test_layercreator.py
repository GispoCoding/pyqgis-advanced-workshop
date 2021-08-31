from pathlib import Path

import pytest as pytest
from qgis._core import QgsCoordinateReferenceSystem
from qgis.core import QgsGeometry

from testplugin.core.layercreator import LayerCreator
from testplugin.qgis_plugin_tools.tools.layers import LayerType
from testplugin.qgis_plugin_tools.tools.resources import root_path

BBOX = (
    "POLYGON((23.5037 61.3199, 25.6954 61.3199, "
    "25.6954 60.3243, 23.5037 60.3243, 23.5037 61.3199))"
)


@pytest.fixture
def point_geojson():
    path = Path(root_path("test", "data", "satamat.geojson"))
    with open(path) as f:
        return f.read()


@pytest.fixture
def lines_geojson():
    path = Path(root_path("test", "data", "viivat.geojson"))
    with open(path) as f:
        return f.read()


@pytest.fixture
def polygons_geojson():
    path = Path(root_path("test", "data", "polygons.geojson"))
    with open(path) as f:
        return f.read()


@pytest.fixture
def layer_creator():
    return LayerCreator("EPSG:4326", "EPSG:3067")


@pytest.mark.parametrize(
    "attributes,buffer,expected_wkt",
    (
        (
            [],
            0.0,
            (
                "Polygon ((312867 6803432, 430154 6799118, 427949 6688241, 306957 6692648, "
                "312867 6803432))"
            ),
        ),
        (["attr1", 1, True], 20.0, None),
    ),
)
def test_feature_from_wkt(layer_creator, attributes, buffer, expected_wkt):
    feature = layer_creator.feature_from_wkt(BBOX, attributes, buffer)
    assert feature.isValid()
    assert feature.attributes() == attributes
    geometry: QgsGeometry = feature.geometry()
    if expected_wkt is not None:
        assert geometry.asWkt(0) == expected_wkt


@pytest.mark.parametrize(
    "wkt_strings,layer_type,buffer",
    (
        (["Point(28 62)"], LayerType.Point, 0.0),
        ([BBOX], LayerType.Polygon, 0.0),
        (["Point(28 62)", "Point(0 0)"], LayerType.Point, 0.0),
        (["Point(28 62)"], LayerType.Point, 2.3),
    ),
)
def test_layer_from_wkt(layer_creator, wkt_strings, layer_type, buffer):
    layer = layer_creator.layer_from_wkt("layer", layer_type, wkt_strings, buffer)
    crs: QgsCoordinateReferenceSystem = layer.crs()
    assert layer.isValid()
    assert crs.authid() == "EPSG:3067"
    assert layer.featureCount() == len(wkt_strings)
    actual_layer_type = LayerType.from_layer(layer)
    if buffer != 0.0:
        assert actual_layer_type == LayerType.Polygon
    else:
        assert actual_layer_type == layer_type


@pytest.mark.parametrize(
    "geojson_str,expected_layer_type",
    (
        ("point_geojson", LayerType.Point),
        ("lines_geojson", LayerType.Line),
        ("polygons_geojson", LayerType.Polygon),
    ),
)
def test_layer_from_geojson(layer_creator, geojson_str, expected_layer_type, request):
    geojson_str = request.getfixturevalue(geojson_str)
    layer = layer_creator.layer_from_geojson("layer", geojson_str)
    assert LayerType.from_layer(layer) == expected_layer_type
    assert layer.isValid()
    assert layer.featureCount() >= 16
