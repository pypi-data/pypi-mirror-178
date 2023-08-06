#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from evadevice import EvaDevice
from .param import DriverType, DeviceButton
from ..utils.logger import get_logger

logger = get_logger("evadevice")


def evadevice_init():
    """Initializes a Global EvaDevice Client."""

    global eva_device
    serial = os.environ.get("serial")
    eva_device = EvaDevice(serial, airtest=True)


def image_resolution(_d: EvaDevice, max_size: int = 800):
    """Return WeAutomator image resolution.

    :param _d: EvaDevice Client.
    :param max_size: screen resolution max size when recording.
    """

    _w, _h = _d.screen_info()
    w, h = None, None
    if _w < _h:
        w, h = _w * max_size / _h, max_size
    else:
        w, h = max_size, _h * max_size / _w
    return w, h


def start_app(pkg_name: str):
    """Launch application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.app_start(pkg_name)


def press(key_code: DeviceButton):
    """Perform keyevent on the device.

    :param key_code: int 
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.key_event(key_code)


def install_app(path_or_url: str, *args, **kwargs):
    """Install application.

    :param path_or_url: local path or url.
    :param nolaunch: do not launch app after install.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.app_install(path_or_url, *args, **kwargs)


def uninstall_app(pkg_name: str):
    """Uninstall application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.app_uninstall(pkg_name)


def restart_app(pkg_name: str):
    """Stop application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.app_stop(pkg_name)


def input_text(text, enter: bool = True, *args, **kwargs):
    """Type a given text.

    :param text: text to be type
    """

    if 'eva_device' not in dir():
        evadevice_init()
    eva_device.input_text(text, enter=enter)


def find(loc, by: DriverType, timeout: int = 20):
    """Wait to match the Template on the device screen.

    :param loc: pic path/url or text.
    :param by: DriverType.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    pos = None
    if by == DriverType.POS:
        pos = loc
    elif by == DriverType.CV:
        pos = eva_device.find_by_cv(path_or_url=f"./data/img/{loc}",
                                    timeout=timeout,
                                    resolution=image_resolution(eva_device))
    elif by == DriverType.OCR:
        pos = eva_device.find_by_ocr(loc, timeout=timeout)
    return pos


def click(loc, by: DriverType, timeout: int = 20, *args, **kwargs):
    """Perform the touch action on the device screen.

    :param loc: pic path/url or text.
    :param by: DriverType.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    if by == DriverType.POS:
        eva_device.airtest_touch(loc)
    elif by == DriverType.CV:
        eva_device.click_by_cv(path_or_url=f"./data/img/{loc}",
                               timeout=timeout,
                               resolution=image_resolution(eva_device))
    elif by == DriverType.OCR:
        eva_device.click_by_ocr(loc, timeout=timeout)


def double_click(loc, by: DriverType, timeout: int = 20, *args, **kwargs):
    """Perform double click.

    :param loc: pic path/url or text.
    :param by: DriverType.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    pos = find(loc, by, timeout)
    eva_device.airtest_double_click(pos)


def long_click(loc, by: DriverType, timeout: int = 20, duration: float = 1, *args, **kwargs):
    """Perform double click.

    :param loc: pic path/url or text.
    :param by: DriverType.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in dir():
        evadevice_init()
    pos = find(loc, by, timeout)
    eva_device.airtest_swipe(v1=pos, duration=duration)


def slide(loc_from, loc_to, by: DriverType, timeout: int = 20, velocity: float = 0.01, *args, **kwargs):
    """Perform the swipe action on the device screen.

    :param loc_from: the start point of swipe.
    :param loc_to: the end point of swipe.
    :param by: DriverType.
    :param timeout: time interval to wait for the match, default is 20.
    :param velocity: velocity.
    """

    pos_from = find(loc_from, by, timeout)
    pos_to = find(loc_to, by, timeout)
    eva_device.airtest_swipe(v1=pos_from, v2=pos_to, duration=velocity)
