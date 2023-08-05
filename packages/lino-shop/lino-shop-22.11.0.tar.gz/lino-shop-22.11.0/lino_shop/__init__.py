# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is the main module of Lino Shop.

.. autosummary::
   :toctree:

   lib
   projects


"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO.get('version')

intersphinx_urls = dict(docs="https://lino-framework.gitlab.io/shop/")
srcref_url = 'https://gitlab.com/lino-framework/shop/blob/master/%s'
doc_trees = ['docs']
