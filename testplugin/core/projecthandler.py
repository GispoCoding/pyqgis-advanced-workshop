import logging
from pathlib import Path

from qgis.core import QgsProject

from testplugin.qgis_plugin_tools.tools.resources import plugin_name

LOGGER = logging.getLogger(plugin_name())


class ProjectHandler:
    def __init__(self, overwrite_file: bool) -> None:
        self._overwrite_file = overwrite_file

    def save_project(self, file_path: Path) -> bool:
        if not file_path.exists() or self._overwrite_file:
            LOGGER.info(f"Saving project to the file {file_path}")
            succeeded = QgsProject.instance().write(str(file_path))
            return succeeded
        raise FileExistsError(f"File {file_path} already exists!")

    def load_project(self, file_path: Path) -> bool:
        if file_path.exists():
            LOGGER.info(f"Loading project from a file {file_path}")
            project = QgsProject.instance()
            project.clear()
            succeeded = project.read(str(file_path))
            return succeeded
        else:
            raise FileNotFoundError(f"File {file_path} does not exist!")
