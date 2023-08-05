# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-shop',
    version='22.11.0',
    install_requires=['lino-xl'],
    description=("A Lino for managing a webshop"),
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/shop",
    license_files=['COPYING'],
    test_suite='tests')

SETUP_INFO.update(long_description="""
Lino Shop is a customizable management system for web shops.

- Project homepage: https://gitlab.com/lino-framework/shop

- Documentation:
  https://lino-framework.gitlab.io/shop/

- For *introductions* and *commercial information* 
  please see `www.saffre-rumma.net
  <https://www.saffre-rumma.net>`__.

""")

SETUP_INFO.update(classifiers="""
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Office/Business
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System
""".format(**SETUP_INFO).strip().splitlines())
SETUP_INFO.update(packages=[
    'lino_shop',
    'lino_shop.lib',
    'lino_shop.lib.products',
    'lino_shop.lib.products.fixtures',
    'lino_shop.lib.shop',
    'lino_shop.lib.shop.fixtures',
    'lino_shop.projects',
    'lino_shop.projects.shop1',
    'lino_shop.projects.shop1.tests',
])

SETUP_INFO.update(message_extractors={
    'lino_shop': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

l = add_package_data('lino_shop.lib.shop')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
