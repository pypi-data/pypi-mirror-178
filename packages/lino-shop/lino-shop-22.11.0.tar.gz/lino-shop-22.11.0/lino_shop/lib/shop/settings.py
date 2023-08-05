# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.projects.std.settings import *
from lino_shop import SETUP_INFO

class Site(Site):

    verbose_name = "Lino Shop"
    description = SETUP_INFO['description']
    version = SETUP_INFO['version']
    url = SETUP_INFO['url']

    demo_fixtures = 'std few_countries minimal_ledger \
    demo demo2 demo3 checkdata'.split()

    user_types_module = 'lino_shop.lib.shop.user_types'
    workflows_module = 'lino_shop.lib.shop.workflows'
    default_build_method = 'weasy2pdf'
    default_ui = "lino_react.react"

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino_shop.lib.shop'
        yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino_xl.lib.countries'
        yield 'lino_xl.lib.contacts'
        #~ yield 'lino_xl.lib.households'

        yield 'lino_xl.lib.excerpts'

        # yield 'lino_xl.lib.outbox'
        yield 'lino_xl.lib.albums'
        # yield 'lino.modlib.files'
        yield 'lino.modlib.publisher'
        yield 'lino.modlib.weasyprint'
        yield 'lino.modlib.export_excel'
        # yield 'lino.modlib.tinymce'
        # yield 'lino.modlib.wkhtmltopdf'

        # ledger must come before sales because its demo fixture
        # creates journals (?)

        # yield 'lino_xl.lib.sepa'
        # yield 'lino_xl.lib.vat'
        # yield 'lino.modlib.ledger'
        yield 'lino_shop.lib.products'
        yield 'lino_xl.lib.sales'
        # yield 'lino_xl.lib.invoicing'
        # yield 'lino_xl.lib.ledger'
        # yield 'lino_xl.lib.finan'
        # yield 'lino_xl.lib.bevat'
        # yield 'lino_xl.lib.sheets'
        yield 'lino_xl.lib.shopping'

    def get_plugin_configs(self):
        """
        Change the default value of certain plugin settings.

        """
        yield super(Site, self).get_plugin_configs()
        yield ('countries', 'hide_region', True)
        yield ('countries', 'country_code', 'BE')
        # yield ('ledger', 'use_pcmn', True)
        yield ('products', 'menu_group', 'sales')
        yield ('users', 'allow_online_registration', True)
        # yield ('ledger', 'sales_method', 'pos')
        yield ('ledger', 'has_payment_methods', True)
        # yield ('invoicing', 'voucher_model', 'sales.CashInvoice')
        # yield ('invoicing', 'voucher_type', 'sales.CashInvoicesByJournal')
