# type: ignore
# flake8: noqa ANN201
"""
This class contains fixtures and common helper function to keep the test files shorter

pytest-qgis (https://pypi.org/project/pytest-qgis) contains the following helpful fixtures:

* qgis_app initializes and returns fully configured QgsApplication.
  This fixture is called automatically on the start of pytest session.
* qgis_canvas initializes and returns QgsMapCanvas
* qgis_iface returns mocked QgsInterface
* new_project makes sure that all the map layers and configurations are removed.
  This should be used with tests that add stuff to QgsProject.

"""
from pathlib import Path

import pytest
from qgis._core import QgsVectorLayer

from testplugin.qgis_plugin_tools.tools.resources import root_path


@pytest.fixture(scope="session")
def geopackage():
    path_to_gpkg = Path(root_path("test", "data", "data.gpkg"))
    assert path_to_gpkg.exists()
    return path_to_gpkg


@pytest.fixture(scope="session")
def nasa_tiff_path():
    path_to_tiff = Path(
        root_path(
            "test",
            "data",
            "nasa_neo_chrolophyll_concentration_2018-03-01_rgb_360x180.TIFF",
        )
    )
    assert path_to_tiff.exists()
    return str(path_to_tiff)


@pytest.fixture
def ne_finland_points_path(geopackage):
    name = "ne_10m_populated_places_suomi"
    return f"{geopackage}|layername={name}"


@pytest.fixture
def ne_finland_points(ne_finland_points_path):
    layer = QgsVectorLayer(ne_finland_points_path, "ne_finland_points", "ogr")
    assert layer.isValid()
    return layer


@pytest.fixture
def sample_wfs_url():
    return (
        "pagingEnabled='true' "
        "preferCoordinatesForWfsT11='false' "
        "restrictToRequestBBOX='1' srsname='EPSG:3067' "
        "typename='avoindata:Varoitusvalot_piste' "
        "url='http://kartta.hel.fi/ws/geoserver/avoindata/wfs' "
        "version='auto'"
    )


@pytest.fixture
def sample_wms_url():
    return (
        "url=http://kartta.hel.fi/ws/geoserver/avoindata/wms&"
        "layers=avoindata:Kiinteistokartta&"
        "styles&"
        "contextualWMSLegend=0&crs=EPSG:3067&"
        "dpiMode=7&featureCount=10&format=image/png"
    )


@pytest.fixture
def sample_wmts_url():
    return (
        "url=https://tiles.maps.eox.at/wmts?"
        "SERVICE%3DWMTS%26REQUEST%3DGetCapabilities&"
        "contextualWMSLegend=0&"
        "crs=EPSG:4326&"
        "dpiMode=7&"
        "featureCount=10&"
        "format=image/jpeg&"
        "layers=s2cloudless-2018&"
        "styles=default&"
        "tileMatrixSet=WGS84"
    )
