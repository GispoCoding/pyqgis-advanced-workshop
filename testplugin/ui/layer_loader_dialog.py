import logging
from typing import Optional

from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import (
    QDialog,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QWidget,
)

from testplugin.core.layerloader import LayerLoader
from testplugin.qgis_plugin_tools.tools.decorations import log_if_fails
from testplugin.qgis_plugin_tools.tools.i18n import tr
from testplugin.qgis_plugin_tools.tools.messages import MsgBar
from testplugin.qgis_plugin_tools.tools.resources import load_ui, plugin_name

FORM_CLASS: QWidget = load_ui("layer_loader.ui")
LOGGER = logging.getLogger(plugin_name())


class LayerLoaderDialog(QDialog, FORM_CLASS):
    file_widget_data: QgsFileWidget
    line_edit_layer: QLineEdit
    line_edit_layer_name: QLineEdit
    r_btn_auto: QRadioButton
    r_btn_raster: QRadioButton
    r_btn_vector: QRadioButton
    r_btn_wfs: QRadioButton
    r_btn_wms: QRadioButton
    r_btn_wmts: QRadioButton
    btn_load_file: QPushButton
    btn_load_interface: QPushButton
    text_edit_uri: QPlainTextEdit

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
        self.layer_loader = LayerLoader(True)

        self.btn_load_file.clicked.connect(self._load_layer_from_file)
        self.btn_load_interface.clicked.connect(self._load_layer_from_interface)

    @log_if_fails
    def _load_layer_from_file(self) -> None:
        layer_name = self._get_layer_name()
        file_path = self._get_file_path()
        if self.r_btn_auto.isChecked():
            success = self.layer_loader.load_layer(layer_name, file_path)
        elif self.r_btn_vector.isChecked():
            success = self.layer_loader.load_vector_layer(layer_name, file_path)
        else:
            success = self.layer_loader.load_raster_layer(layer_name, file_path)

        if success:
            MsgBar.info(tr("Layer {} loaded successfully", layer_name), success=True)
        else:
            MsgBar.warning(
                tr("Could not load layer {} from {}", layer_name, file_path),
                tr("Check if the file is valid"),
            )

    @log_if_fails
    def _load_layer_from_interface(self) -> None:
        layer_name = self._get_layer_name()
        uri = self.text_edit_uri.toPlainText()

        if self.r_btn_wfs.isChecked():
            success = self.layer_loader.load_wfs_layer(layer_name, uri)
        elif self.r_btn_wms.isChecked():
            success = self.layer_loader.load_wms_layer(layer_name, uri)
        else:
            success = self.layer_loader.load_wmts_layer(layer_name, uri)

        if success:
            MsgBar.info(tr("Layer {} loaded successfully", layer_name), success=True)
        else:
            MsgBar.warning(
                tr("Could not load layer {} from {}", layer_name, uri),
                tr("Check if the uri is valid"),
            )

    def _get_layer_name(self) -> str:
        layer_name = self.line_edit_layer_name.text()
        if layer_name != "":
            return layer_name
        else:
            raise ValueError(tr("Layer has to have a name"))

    def _get_file_path(self) -> str:

        file_path = self.file_widget_data.filePath()
        if file_path != "":
            layer = self.line_edit_layer.text()
            if layer:
                file_path += f"|layername={layer}"
            return file_path
        else:
            raise ValueError(tr("Set file path first!"))
