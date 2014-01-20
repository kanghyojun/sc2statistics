# -*- coding: utf-8 -*-
import logging

__all__ = 'get_logger',

def get_logger():
    format_ = logging.Formatter('%(asctime)-15s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(format_)
    logger.addHandler(ch)
    return logger
