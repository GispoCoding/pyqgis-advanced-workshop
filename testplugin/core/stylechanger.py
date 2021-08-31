from qgis.core import QgsSingleSymbolRenderer, QgsSymbol, QgsVectorLayer
from qgis.PyQt.QtGui import QColor


class StyleChanger:
    @staticmethod
    def modify_layer_style(
        layer: QgsVectorLayer, color: QColor, opacity: float
    ) -> None:
        renderer: QgsSingleSymbolRenderer = layer.renderer()
        symbol: QgsSymbol = renderer.symbol()
        symbol.setColor(color)
        symbol.setOpacity(opacity)
        layer.triggerRepaint()
