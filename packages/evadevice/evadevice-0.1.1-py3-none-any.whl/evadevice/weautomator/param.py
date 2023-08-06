#! /usr/bin/env python
# -*- coding: utf-8 -*-
class DriverType(object):
    """WeAutomator DriverType."""

    POS = 0
    OCR = 2
    CV = 3


class DeviceButton(object):
    """DeviceButton."""

    HOME = 3
    VOLUME_UP = 24
    VOLUME_DOWN = 25

    # for Android special
    BACK = 4
    POWER = 26
    DEL = 67
    FORWARD_DEL = 112
    MENU = 82
    RECENT_APP = 187
    SLEEP = 223
    WAKE_UP = 224
