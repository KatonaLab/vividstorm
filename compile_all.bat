pyrcc4 resources\main_resources.qrc -o views\main_resources_rc.py
start "" pyuic4 gui\main_window.ui -o views\main_window.py
start "" pyuic4 gui\dialog_error.ui -o views\dialog_error.py
start "" pyuic4 gui\dialog_about.ui -o views\dialog_about.py
start "" pyuic4 gui\dialog_help.ui -o views\dialog_help.py
start "" pyuic4 gui\dialog_loading.ui -o views\dialog_loading.py
start "" pyuic4 gui\dialog_scale.ui -o views\dialog_scale.py
start "" pyuic4 gui\dialog_tool_active_contour.ui -o views\dialog_tool_active_contour.py
start "" pyuic4 gui\dialog_tool_analysis.ui -o views\dialog_tool_analysis.py
start "" pyuic4 gui\dialog_tool_lut.ui -o views\dialog_tool_lut.py
start "" pyuic4 gui\dialog_tool_positioning.ui -o views\dialog_tool_positioning.py
start "" pyuic4 gui\dialog_view_3d.ui -o views\dialog_view_3d.py
start "" pyuic4 gui\dialog_view_dots.ui -o views\dialog_view_dots.py
start "" pyuic4 gui\dialog_view_gaussian.ui -o views\dialog_view_gaussian.py
start "" pyuic4 gui\dialog_imageregistration.ui -o views\dialog_tool_imageregistration.py