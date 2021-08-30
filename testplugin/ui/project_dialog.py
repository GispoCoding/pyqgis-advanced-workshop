import logging
from pathlib import Path
from typing import Optional

from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QDialog, QPushButton, QWidget

from testplugin.core.projecthandler import ProjectHandler
from testplugin.qgis_plugin_tools.tools.decorations import log_if_fails
from testplugin.qgis_plugin_tools.tools.i18n import tr
from testplugin.qgis_plugin_tools.tools.messages import MsgBar
from testplugin.qgis_plugin_tools.tools.resources import load_ui, plugin_name

FORM_CLASS: QWidget = load_ui("project_handler.ui")
LOGGER = logging.getLogger(plugin_name())


class ProjectDialog(QDialog, FORM_CLASS):
    file_widget_load: QgsFileWidget
    file_widget_save: QgsFileWidget
    btn_load: QPushButton
    btn_save: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)

        self.btn_load.clicked.connect(self._load)
        self.btn_save.clicked.connect(self._save)
        self.project_handler = ProjectHandler(True)

    @log_if_fails
    def _load(self) -> None:
        file_path_str = self.file_widget_load.filePath()
        if file_path_str != "":
            file_path = Path(file_path_str)
            succeeded = self.project_handler.load_project(file_path)
            if succeeded:
                MsgBar.info(
                    tr("Project {} opened successfully", file_path_str), success=True
                )
            if not succeeded:
                MsgBar.error(
                    tr("Could not open project {}", file_path_str),
                    tr("Please check if the file is a valid QGIS project file"),
                )
        else:
            MsgBar.warning(tr("Select a file to load"))

    @log_if_fails
    def _save(self) -> None:
        file_path_str = self.file_widget_save.filePath()
        if file_path_str != "":
            file_path = Path(file_path_str)
            succeeded = self.project_handler.save_project(file_path)
            if succeeded:
                MsgBar.info(
                    tr("Project saved successfully to {}", file_path_str), success=True
                )
            if not succeeded:
                MsgBar.error(
                    tr("Could not save the project to {}", file_path_str),
                    tr("Please check if the path is valid"),
                )
        else:
            MsgBar.warning(tr("Select a file to save first"))
