# -*- coding: UTF-8 -*-
# Copyright 2021-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
The main plugin for Lino Shop.

"""
from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Lino Shop")

    def get_dashboard_items(self, user):
        yield self.site.models.products.Books
