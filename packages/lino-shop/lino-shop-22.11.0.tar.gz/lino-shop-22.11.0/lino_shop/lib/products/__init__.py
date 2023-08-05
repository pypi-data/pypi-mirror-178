# -*- coding: UTF-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
An extension of :mod:`lino_xl.lib.products`
"""

from lino_xl.lib.products import Plugin

class Plugin(Plugin):

    extends_models = ['Product']

#     needs_plugins = ['lino_cosi.lib.cosi']

    def setup_config_menu(self, site, user_type, m):
        super(Plugin, self).setup_config_menu(site, user_type, m)
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('products.Authors')

    def get_quicklinks(self):
        for pt in self.site.models.products.ProductTypes.get_list_items():
            yield pt.table_name
        # for pc in self.site.models.products.Category.objects.all():
        #     # yield self.site.models.products.ProductsByCategory.request(master_instance=pc)
        #     yield dict(params=dict(master_instance=pc),
        #         action='products.ProductsByCategory', label=str(pc))
