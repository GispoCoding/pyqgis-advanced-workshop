import logging
from typing import Optional

from qgis.core import QgsCoordinateReferenceSystem, QgsProject
from qgis.gui import QgsProjectionSelectionWidget
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDoubleSpinBox,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)

from testplugin.core.layercreator import LayerCreator
from testplugin.qgis_plugin_tools.tools.decorations import log_if_fails
from testplugin.qgis_plugin_tools.tools.i18n import tr
from testplugin.qgis_plugin_tools.tools.layers import LayerType
from testplugin.qgis_plugin_tools.tools.resources import load_ui, plugin_name

FORM_CLASS: QWidget = load_ui("layer_creator.ui")
LOGGER = logging.getLogger(plugin_name())


class LayerCreatorDialog(QDialog, FORM_CLASS):
    crs_src: QgsProjectionSelectionWidget
    crs_target: QgsProjectionSelectionWidget
    text_edit_wkt: QPlainTextEdit
    btn_load_wkt: QPushButton
    text_edit_geojson: QPlainTextEdit
    btn_load_geojson: QPushButton
    line_edit_layer_name: QLineEdit
    spin_box_buffer = QDoubleSpinBox

    default_src_crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem(
        "EPSG:4326"
    )
    default_target_crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem(
        "EPSG:3067"
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
        self.crs_src.setCrs(self.default_src_crs)
        self.crs_target.setCrs(self.default_target_crs)
        self.btn_load_wkt.clicked.connect(self._create_wkt_layer)
        self.btn_load_geojson.clicked.connect(self._create_geojson_layer)

    @property
    def _layer_creator(self) -> LayerCreator:
        return LayerCreator(self.crs_src.crs().authid(), self.crs_target.crs().authid())

    @log_if_fails
    def _create_wkt_layer(self) -> None:
        wkt_string = self.text_edit_wkt.toPlainText()
        wkt_strings = [wkt.strip() for wkt in wkt_string.split("|")]
        if "POLYGON" in wkt_string.upper():
            layer_type = LayerType.Point
        elif "LINE" in wkt_string.upper():
            layer_type = LayerType.Line
        elif "POINT" in wkt_string.upper():
            layer_type = LayerType.Point
        else:
            raise ValueError(tr("Invalid WKT!"))

        layer = self._layer_creator.layer_from_wkt(
            self._get_layer_name(),
            layer_type,
            wkt_strings,
            self.spin_box_buffer.value(),
        )
        QgsProject.instance().addMapLayer(layer)

    @log_if_fails
    def _create_geojson_layer(self) -> None:
        geojson_string = self.text_edit_geojson.toPlainText()
        layer = self._layer_creator.layer_from_geojson(
            self._get_layer_name(), geojson_string
        )
        QgsProject.instance().addMapLayer(layer)

    def _get_layer_name(self) -> str:
        layer_name = self.line_edit_layer_name.text()
        if layer_name != "":
            return layer_name
        else:
            raise ValueError(tr("Layer has to have a name"))
