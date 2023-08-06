#!/usr/bin/env python

TEMPLATE_DIR = None

from .config import read_config, save_config

read_config()

from .papers import paper_root, get_template, to_pdf, create
from .templates import all_templates, find_template, install_template, update_template
from .__main__ import main