import os
import rospkg
import rospy
import sys
import roslaunch

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

from PyQt5 import QtCore, QtGui

from std_msgs.msg import String

import time

class LightBeaconGui(Plugin):

    def __init__(self, context):
        super(LightBeaconGui, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('LightButtonGui')
        self.rp = rospkg.RosPack()

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which is a sibling of this file
        # in this example the .ui and .py file are in the same folder
        ui_file = os.path.join(self.rp.get_path('light_beacon_gui'), 'resource', 'LightBeaconGui.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('LightBeaconGui')
        # Show _widget.windowTitle on left-top of each plugin (when
        # it's set in _widget). This is useful when you open multiple
        # plugins at once. Also if you open multiple instances of your
        # plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

        self._widget.pat1_disp.setStyleSheet("background-color: white")
        self._widget.pat2_disp.setStyleSheet("background-color: white")
        self._widget.pat3_disp.setStyleSheet("background-color: white")

        rospy.Subscriber("/light_beacon_readings", String, self.beaconReadCallback)

    def beaconReadCallback(self, msg):
        if len(msg.data) == 3:
            for n in range(len(msg.data)):
                c = msg.data[n]
                if n == 0:
                    if c == "r":
                        self._widget.pat1_disp.setStyleSheet("background-color: red")
                    elif c == "g":
                        self._widget.pat1_disp.setStyleSheet("background-color: green")
                    elif c == "b":
                        self._widget.pat1_disp.setStyleSheet("background-color: blue")
                    else:
                        self._widget.pat1_disp.setStyleSheet("background-color: white")
                elif n == 1:
                    if c == "r":
                        self._widget.pat2_disp.setStyleSheet("background-color: red")
                    elif c == "g":
                        self._widget.pat2_disp.setStyleSheet("background-color: green")
                    elif c == "b":
                        self._widget.pat2_disp.setStyleSheet("background-color: blue")
                    else:
                        self._widget.pat2_disp.setStyleSheet("background-color: white")
                elif n == 2:
                    if c == "r":
                        self._widget.pat3_disp.setStyleSheet("background-color: red")
                    elif c == "g":
                        self._widget.pat3_disp.setStyleSheet("background-color: green")
                    elif c == "b":
                        self._widget.pat3_disp.setStyleSheet("background-color: blue")
                    else:
                        self._widget.pat3_disp.setStyleSheet("background-color: white")




    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
