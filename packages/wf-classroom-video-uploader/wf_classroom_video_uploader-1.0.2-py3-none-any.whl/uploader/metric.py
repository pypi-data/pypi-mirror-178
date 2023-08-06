import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import time

from influx_line_protocol import Metric


METRICS_LOG_DIR = Path(os.environ.get("METRICS_LOG", "/var/log/wf_metrics"))

metlogger = logging.getLogger("wf_metrics")
if not METRICS_LOG_DIR.exists():
    METRICS_LOG_DIR.mkdir()
path = METRICS_LOG_DIR / f"{os.environ.get('METRICS_NAME', 'control-uploader')}.log"
metlogger.setLevel(logging.INFO)
handy = RotatingFileHandler(path, maxBytes=20000000, backupCount=5)
handy.setFormatter(logging.Formatter())
metlogger.addHandler(handy)

def emit(name, values, tags=None):
    metric = Metric(name)
    metric.with_timestamp(time.time() * 1000000000)
    if tags is None:
        tags = {"tag": "team"}
    for tag in tags:
        metric.add_tag(tag, tags[tag])
    for value in values:
        metric.add_value(value, values[value])
    metlogger.info(metric)
