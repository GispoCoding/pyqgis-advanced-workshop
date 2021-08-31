import pytest as pytest
from PyQt5.QtGui import QColor
from qgis.PyQt.QtCore import Qt

from testplugin.core.stylechanger import StyleChanger


@pytest.fixture
def style_changer(new_project):
    return StyleChanger()


def test_modify_layer_style(style_changer, ne_finland_points):
    style_changer.modify_layer_style(ne_finland_points, QColor(Qt.black), 0.5)
    symbol = ne_finland_points.renderer().symbol()
    assert symbol.color() == QColor(Qt.black)
    assert symbol.opacity() == 0.5
