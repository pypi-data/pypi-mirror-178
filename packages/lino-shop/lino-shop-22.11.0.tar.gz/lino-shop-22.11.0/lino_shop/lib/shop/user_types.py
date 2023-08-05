# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole, SiteAdmin, SiteUser, SiteStaff
from lino.modlib.users.choicelists import UserTypes
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.products.roles import ProductsUser, ProductsStaff
from lino_xl.lib.ledger.roles import LedgerUser, LedgerStaff, LedgerPartner
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from lino.api import _


class Customer(SiteUser, LedgerPartner,
               SepaUser, ExcerptsUser, ProductsUser):
    pass

class Vendor(SiteUser, OfficeUser, LedgerPartner,
             SepaUser, ExcerptsUser, ProductsUser):
    pass

class SiteStaff(SiteStaff, ContactsStaff, OfficeStaff,
                LedgerStaff, LedgerPartner, SepaStaff, ExcerptsStaff, ProductsStaff):
    pass

class SiteAdmin(SiteAdmin, ContactsStaff, OfficeStaff,
                LedgerStaff, LedgerPartner, SepaStaff, ExcerptsStaff, ProductsStaff):
    pass

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),     UserRole,  'anonymous', readonly=True)
add('100', _("Customer"),      Customer,  'user')
add('200', _("Vendor"),        Vendor,    'vendor')
add('500', _("Staff"),         SiteStaff, 'staff')
add('900', _("Administrator"), SiteAdmin, 'admin')
