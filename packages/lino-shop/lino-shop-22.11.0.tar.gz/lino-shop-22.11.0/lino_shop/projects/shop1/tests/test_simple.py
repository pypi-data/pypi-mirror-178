# -*- coding: utf-8 -*-
# Copyright 2011-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_shop1

Or::

  $ go shop
  $ cd lino_shop/projects/shop1
  $ python manage.py test tests.test_simple

"""

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.utils.instantiator import create_row
from lino.api import rt


class SimpleTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        User = rt.models.users.User
        UserTypes = rt.models.users.UserTypes
        Product = rt.models.products.Product

        robin = create_row(User, username='robin',
                           user_type=UserTypes.admin, language="en")

        foo = create_row(Product, name='Foo')
