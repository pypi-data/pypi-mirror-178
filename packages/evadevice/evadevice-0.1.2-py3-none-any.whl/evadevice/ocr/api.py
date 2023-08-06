#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import difflib
from evadevice import EvaDevice
from .model.ppocr_v3 import ppocr_v3
from ..utils.logger import get_logger

logger = get_logger("evadevice")


def loop_find_by_ocr(_d: EvaDevice, query: str, timeout: int = 20, interval=0.5):
    """Search for text template in the screen until timeout.

    :param query: text template to be found in screenshot.
    :param timeout: time interval how long to look for the image template.
    :param interval: sleep interval before next attempt to find the image template.
    """

    start_time = time.time()
    while True:
        screen = _d.airtest.snapshot(filename=None)

        if screen is None:
            logger.warn("Screen is None, may be locked.")
        else:
            ocr_result = ppocr_v3.predict(screen)
            ocr_result_text = [i.replace('\r', '') for i in ocr_result.text]
            list_text = [i for i in ocr_result_text if i != '']
            match_text = difflib.get_close_matches(query, list_text, 1,
                                                   cutoff=0.6)
            if len(match_text) > 0:
                text = match_text[0]
                index = ocr_result_text.index(text)
                boxes = ocr_result.boxes[index]
                pos_x = (boxes[0] + boxes[2] + boxes[4] + boxes[6]) / 4
                pos_y = (boxes[1] + boxes[3] + boxes[5] + boxes[7]) / 4
                logger.info(f"Text ``{query}`` founded in screen.")
                logger.info(f"Text ``{text}`` pos: ({pos_x}, {pos_y}).")
                return (pos_x, pos_y)

        if (time.time() - start_time) > timeout:
            print("ocr found:")
            print(ocr_result)
            raise Exception(f"Text ``{query}`` not found in screen.")
        else:
            time.sleep(interval)
