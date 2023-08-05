# -*- coding: UTF-8 -*-
# Copyright 2010-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.modlib.users.choicelists import UserTypes
from lino.mixins.human import parse_name



def user(lang, user_type, name, **kw):
    kw.update(**parse_name(name))
    kw.update(username=kw['first_name'].lower())
    kw.update(user_type=user_type)
    kw.update(email=settings.SITE.demo_email)
    kw.update(language=lang)
    return settings.SITE.user_model(**kw)


def objects():
    # logger.info("20150323 %s", settings.SITE.languages)
    yield user('en', 'user', "Joe Doe")
    yield user('en', 'vendor', "John Doe")
    yield user('en', 'staff', "Jill Doe")
