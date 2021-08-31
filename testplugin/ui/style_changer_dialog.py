import logging
from typing import Optional

from qgis.gui import QgsColorButton, QgsMapLayerComboBox, QgsOpacityWidget
from qgis.PyQt.QtWidgets import QDialog, QPushButton, QWidget

from testplugin.core.stylechanger import StyleChanger
from testplugin.qgis_plugin_tools.tools.decorations import log_if_fails
from testplugin.qgis_plugin_tools.tools.i18n import tr
from testplugin.qgis_plugin_tools.tools.resources import load_ui, plugin_name

FORM_CLASS: QWidget = load_ui("style_changer.ui")
LOGGER = logging.getLogger(plugin_name())


class StyleChangerDialog(QDialog, FORM_CLASS):
    combo_box_layer: QgsMapLayerComboBox
    color_btn: QgsColorButton
    opacity_slider: QgsOpacityWidget
    btn_apply: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
        self.btn_apply.clicked.connect(self._set_style)

    @log_if_fails
    def _set_style(self) -> None:
        layer = self.combo_box_layer.currentLayer()
        color = self.color_btn.color()
        opacity = self.opacity_slider.opacity()
        if layer is None:
            raise ValueError(tr("Select layer to begin"))
        if color is None:
            raise ValueError(tr("Select color to begin"))

        StyleChanger.modify_layer_style(layer, color, opacity)
