# coding =utf-8

# !/usr/bin/python
import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/jungipark/service/calendar-api")

from app import create_app

application = create_app('production')
