#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from evadevice import d, EvaDevice
from ..utils.logger import get_logger

logger = get_logger("evadevice")


def evadevice_init():
    """Initializes a Global EvaDevice Client."""

    global eva_device
    serial = os.environ.get("serial")
    assert serial, "Invalid serial, Please Set os.environ['serial']= 'xxxxxx'"
    eva_device = EvaDevice(serial, airtest=True)


def device_list(refresh: bool = False):
    """Return device list.

    :param refresh: refresh global device list.
    """

    return d.device_list(refresh)


def start_watch_device(callback, system: str = "all"):
    """Report device state when changes.

    :param callback: Attaches a callable that will be called when the device state changes.
    :param system: ios or android, default all.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.start_watch_device(callback, system)


def start_auto_confirm(text_pattern: str = None):
    """Start auto confirm for iOS/Android.

    :param text_pattern: pattern to search for.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.start_auto_confirm(text_pattern)


def stop_auto_confirm():
    """Stop auto confirm."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.stop_auto_confirm()


def device_info():
    """Return device info."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.device_info()


def app_list():
    """Return application list."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.app_list()


def app_install(path_or_url: str, *args, **kwargs):
    """Install application.

    :param path_or_url: local path or url.
    :param nolaunch: do not launch app after install.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.app_install(path_or_url, *args, **kwargs)


def app_uninstall(pkg_name: str):
    """Uninstall application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.app_uninstall(pkg_name)


def app_start(pkg_name: str):
    """Launch application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.app_start(pkg_name)


def app_stop(pkg_name: str):
    """Stop application.

    :param pkg_name: package name for Android, bundle_id for iOS.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.app_stop(pkg_name)


def app_current():
    """Return the currently active application."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.app_current()


def push(src: str, dst: str, *args, **kwargs):
    """Push dir and files for iOS/Android.

    :param src: source path.
    :param dst: destination path.
    :param bundle_id: bundle_id for iOS, None for Android.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.push(src, dst, *args, **kwargs)


def pull(src: str, dst: str, *args, **kwargs):
    """Pull dir and files for iOS/Android.

    :param src: source path.
    :param dst: destination path.
    :param bundle_id: bundle_id for iOS, None for Android.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.pull(src, dst, *args, **kwargs)


def start_recording(filename: str):
    """Start video recording.

    :param filename: local filename path.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.start_recording(filename)


def stop_recording():
    """Stop video recording."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.stop_recording()


def screenshot(filename: str):
    """Save screenshot."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.screenshot(filename)


def screen_info():
    """Return screen info."""

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.screen_info()


def unlock_screen(password: str):
    """Unlock Screen for Android.

    :param password: unlock screen password.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.unlock_screen(password)


def key_event(key_code: int):
    """Perform keyevent on the device.

    :param key_code: int 
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.key_event(key_code)


def input_text(text: str, enter: bool = True):
    """Type a given text.

    :param text: text to be type
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.input_text(text, enter)


def find_by_ocr(text: str, timeout: int = 20, interval=0.5):
    """Wait to match the Text Template on the device screen.

    :param text: text template to be found in screenshot.
    :param timeout: time interval how long to look for the image template.
    :param interval: sleep interval before next attempt to find the image template.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.find_by_ocr(text, timeout, interval)


def click_by_ocr(text: str, timeout: int = 20, interval=0.5):
    """Perform the touch action on the device screen.

    :param text: text template to be found in screenshot.
    :param timeout: time interval how long to look for the image template.
    :param interval: sleep interval before next attempt to find the image template.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.click_by_ocr(text, timeout, interval)


def find_by_cv(path_or_url: str, timeout: int = 20, *args, **kwargs):
    """Wait to match the Template on the device screen.

    :param path_or_url: pic path or url.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    return eva_device.find_by_cv(path_or_url, timeout, *args, **kwargs)


def click_by_cv(path_or_url: str, timeout: int = 20, *args, **kwargs):
    """Perform the touch action on the device screen.

    :param path_or_url: pic path or url.
    :param timeout: time interval to wait for the match, default is 20.
    """

    if 'eva_device' not in globals().keys():
        evadevice_init()
    eva_device.click_by_cv(path_or_url, timeout, *args, **kwargs)
