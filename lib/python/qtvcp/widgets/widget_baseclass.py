#!/usr/bin/env python
# qtvcp baseclass
#
# Copyright (c) 2017  Chris Morley <chrisinnanaimo@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# _HalWidgetBase is the base class for most pyQt widgets
# the other subclasses are for simple HAL widget functionality

from PyQt4 import QtCore, QtGui
import hal

###########################
""" Set of base classes """
###########################

class _HalWidgetBase:
    def hal_init(self, comp, name, object, toplevel,PATHS):
        self.hal, self.hal_name = comp, name
        self.QT_OBJECT_ = object
        self.QTVCP_INSTANCE_ = toplevel
        self.PATHS_ = PATHS
        self._hal_init()

    def _hal_init(self):
        """ Child HAL initialization functions """
        pass

class _HalToggleBase(_HalWidgetBase):
    def _hal_init(self):
        self.hal_pin = self.hal.newpin(self.hal_name, hal.HAL_BIT, hal.HAL_OUT)
        self.hal_pin_not = self.hal.newpin(self.hal_name + "-not", hal.HAL_BIT, hal.HAL_OUT)
        self.connect.state_change.connect(lambda data: self.t_update(data))

    def t_update(self,state):
        self.hal_pin.set(bool(state))
        self.hal_pin_not.set(not bool(state))

# reacts to HAL pin changes
class _HalScaleBase(_HalWidgetBase):
    def _hal_init(self):
        self.hal_pin = self.hal.newpin(self.hal_name, hal.HAL_FLOAT, hal.HAL_OUT)
        self.connect.value_changed.connect(lambda data: self.l_update(data))

    def l_update(self, *a):
        self.hal_pin.set(self.get_value())

# reacts to HAL pin changes
class _HalSensitiveBase(_HalWidgetBase):
    def _hal_init(self):
        self.hal_pin = self.hal.newpin(self.hal_name, hal.HAL_BIT, hal.HAL_IN)
        self.hal_pin.value_changed.connect( lambda s: self.setEnabled(s))