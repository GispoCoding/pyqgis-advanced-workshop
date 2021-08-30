from pathlib import Path

import pytest as pytest
from qgis.core import QgsProject

from testplugin.core.projecthandler import ProjectHandler
from testplugin.qgis_plugin_tools.tools.resources import plugin_test_data_path


@pytest.fixture
def project_handler():
    return ProjectHandler(True)


@pytest.fixture
def test_project():
    project = Path(plugin_test_data_path("test_project.qgs"))
    assert project.exists()
    return project


def test_save_project(project_handler, tmp_path):
    qgs_file = tmp_path / "test.qgs"
    succeeded = project_handler.save_project(qgs_file)
    assert succeeded
    assert qgs_file.exists()


def test_load_project(new_project, project_handler, test_project):
    succeeded = project_handler.load_project(test_project)
    assert succeeded
    layers = QgsProject.instance().mapLayers()
    assert len(layers) == 1
