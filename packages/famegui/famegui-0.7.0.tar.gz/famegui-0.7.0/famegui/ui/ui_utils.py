import logging
from datetime import datetime

from PySide2.QtGui import QFont
from PySide2.QtWidgets import  QFormLayout, QScrollArea, QLabel


class GUIConsoleHandler(logging.StreamHandler):

    def __init__(self, form_layout: QFormLayout,
                 scroll_area: QScrollArea):
        logging.StreamHandler.__init__(self)
        super().__init__()
        self._form_layout = form_layout
        self._scroll_area = scroll_area

    def emit(self, record):
        msg = self.format(record)
        labelWidget = QLabel(
            record.levelname + " : " + msg)
        labelWidget.setWordWrap(True)
        labelWidget.setStyleSheet("color: #F5F5F5;")

        font = QFont()
        font.setPointSize(10)
        labelWidget.setFont(font)
        self._form_layout.addRow(labelWidget)
