import pytest as pytest
from qgis.core import QgsProject, QgsVectorLayer

from testplugin.core.layerloader import LayerLoader

TEST_LAYER_NAME = "test_layer"


@pytest.fixture
def layer_loader(new_project) -> LayerLoader:
    return LayerLoader(True)


def test_load_vector_layer(layer_loader, ne_finland_points_path):
    successful = layer_loader.load_vector_layer(TEST_LAYER_NAME, ne_finland_points_path)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_raster_layer(layer_loader, nasa_tiff_path):
    successful = layer_loader.load_raster_layer(TEST_LAYER_NAME, nasa_tiff_path)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_layer_vector(layer_loader, ne_finland_points_path):
    successful = layer_loader.load_layer(TEST_LAYER_NAME, ne_finland_points_path)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_layer_raster(layer_loader, nasa_tiff_path):
    successful = layer_loader.load_layer(TEST_LAYER_NAME, nasa_tiff_path)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_wfs_layer(layer_loader, sample_wfs_url):
    successful = layer_loader.load_wfs_layer(TEST_LAYER_NAME, sample_wfs_url)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_wms_layer(layer_loader, sample_wms_url):
    successful = layer_loader.load_wms_layer(TEST_LAYER_NAME, sample_wms_url)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1


def test_load_wmts_layer(layer_loader, sample_wmts_url):
    successful = layer_loader.load_wmts_layer(TEST_LAYER_NAME, sample_wmts_url)
    layers = QgsProject.instance().mapLayersByName(TEST_LAYER_NAME)
    assert successful
    assert len(layers) == 1
