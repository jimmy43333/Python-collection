import os
import time
import argparse
import sys
import logging

# NOTSET >> DEBUG >> INFO >> WARNING >> ERROR >> CRITICAL
# Handlers   : 負責發送相關的信息到指定目的地
# Formatters : 設置日誌信息最後的規則、結構和內容

def setuplog(filename,mode,level):
    logging.getLogger('').setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename,mode)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)