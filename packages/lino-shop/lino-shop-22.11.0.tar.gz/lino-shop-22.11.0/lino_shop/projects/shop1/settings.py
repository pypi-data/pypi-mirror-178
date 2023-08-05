# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from lino_shop.lib.shop.settings import *


class Site(Site):

    is_demo_site = True
    the_demo_date = datetime.date(2021, 3, 22)
    languages = "en de fr"

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('vat', 'declaration_plugin', 'lino_xl.lib.bevat')
        yield ('countries', 'hide_region', True)
        yield ('countries', 'country_code', 'BE')
        yield ('ledger', 'use_pcmn', True)
        yield ('ledger', 'worker_model', 'contacts.Person')
        yield ('products', 'barcode_driver', 'ean13')
        # yield ('users', 'active_sessions_limit', 1)


    # default_ui = 'lino_react.react'
    # default_ui = 'lino.modlib.extjs'

from lino.core.auth.utils import activate_social_auth_testing

activate_social_auth_testing(globals())

SITE = Site(globals())

DEBUG = True
USE_TZ = True
TIME_ZONE = 'UTC'
