# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import _
from lino.modlib.uploads.choicelists import UploadAreas

UploadAreas.clear()
add = UploadAreas.add_item
add('10', _("Photos"), 'photos')
add('90', _("General"), 'general')
