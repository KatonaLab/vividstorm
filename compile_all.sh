pyrcc5 resources/main_resources.qrc -o views/main_resources_rc.py
pyuic5 gui/main_window.ui -o views/main_window.py --from-imports
pyuic5 gui/dialog_error.ui -o views/dialog_error.py --from-imports
pyuic5 gui/dialog_about.ui -o views/dialog_about.py --from-imports
pyuic5 gui/dialog_help.ui -o views/dialog_help.py --from-imports
pyuic5 gui/dialog_loading.ui -o views/dialog_loading.py --from-imports
pyuic5 gui/dialog_scale.ui -o views/dialog_scale.py --from-imports
pyuic5 gui/dialog_tool_active_contour.ui -o views/dialog_tool_active_contour.py --from-imports
pyuic5 gui/dialog_tool_analysis.ui -o views/dialog_tool_analysis.py --from-imports
pyuic5 gui/dialog_tool_lut.ui -o views/dialog_tool_lut.py --from-imports
pyuic5 gui/dialog_tool_positioning.ui -o views/dialog_tool_positioning.py --from-imports
pyuic5 gui/dialog_view_3d.ui -o views/dialog_view_3d.py --from-imports
pyuic5 gui/dialog_view_dots.ui -o views/dialog_view_dots.py --from-imports
pyuic5 gui/dialog_view_gaussian.ui -o views/dialog_view_gaussian.py --from-imports
pyuic5 gui/dialog_imageregistration.ui -o views/dialog_tool_imageregistration.py --from-imports