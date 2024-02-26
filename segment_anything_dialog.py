# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SegmentAnythingDialog
                                 A QGIS plugin
 Segment Anything From Facebook Research
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-02-24
        git sha              : $Format:%H$
        copyright            : (C) 2024 by INF800
        email                : rakeshark22@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import logging
from datetime import datetime

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QComboBox, QFileDialog, QMessageBox


class InputDataLayerOption:
    FROM_POLYGON = "From Polygons"
    VISIBLE_PART = "Visible Part"
    ENTIRE_LAYER = "Entire Layer"


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "segment_anything_dialog_base.ui")
)


class SegmentAnythingDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SegmentAnythingDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self._model = None
        self.setupUi(self)

        self._create_connections()
        self._setup_input_data_ui()

    def _toggle_polygons_layer_visiblity(self):
        is_visible = (
            self.qmlcbInputDataLayerOption.currentText()
            == InputDataLayerOption.FROM_POLYGON
        )
        self.qmlcbInputDataPolygonsLayer.setVisible(is_visible)
        self.lbInputDataPolygonsLayer.setVisible(is_visible)

    def _load_model_and_display_info(self, abort_if_no_file_path: bool = False):
        # load model
        file_path = self.qleModelPath.text()
        if not file_path and abort_if_no_file_path:
            return

        msg = ""
        try:
            self._model = ...  # TODO: Load model
            msg = msg + f"✅ Model loaded successfully on: {datetime.now()}"
        except Exception as e:
            msg = (
                "❌ Error! Failed to load the model.\n"
                "Please make sure downloaded model is usable."
            )
            logging.exception(msg)

            length_limit = 300
            exception_msg = (
                (str(e)[:length_limit] + "..") if len(str(e)) > length_limit else str(e)
            )
            msg = msg + f"\n\nException: {exception_msg}"
            QMessageBox.critical(self, "Error!", msg)

        self.lbModelInfoValue.setText(msg)

    def _browse_model_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Model ONNX file...",
            os.path.expanduser("~"),
            "All files (*.*);; ONNX files (*.onnx)",
        )
        if file_path:
            self.qleModelPath.setText(file_path)
            self._load_model_and_display_info()

    def _run_inference(self):
        msg = (
            f"Selected vector data (image): {str(self.qmlcbInputDataLayer.currentLayer())}\n"
            f"Selected Model: {self._model}\n\n"
        )

        msg += "⌛ Running...\n"
        self.lbRunStatusValue.setText(msg)

        msg += "✅ Done!"
        self.lbRunStatusValue.setText(msg)

    def _create_connections(self):
        # Input vector / raster data
        self.qmlcbInputDataLayerOption.currentIndexChanged.connect(
            self._toggle_polygons_layer_visiblity
        )
        # Load ONNX Model
        self.pbBrowseModel.clicked.connect(self._browse_model_path)
        self.pbLoadOrReloadModel.clicked.connect(self._load_model_and_display_info)
        # Run Inference
        self.pbRunInference.clicked.connect(self._run_inference)

    def _setup_input_data_ui(self):
        layer_options = [
            InputDataLayerOption.VISIBLE_PART,
            InputDataLayerOption.ENTIRE_LAYER,
            InputDataLayerOption.FROM_POLYGON,
        ]

        for option in layer_options:
            self.qmlcbInputDataLayerOption.addItem(option)
