# -*- coding: UTF-8 -*-
# Copyright 2009-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.instantiator import Instantiator
from lino_xl.lib.products.choicelists import ProductTypes

from lino.mixins.human import parse_name

from lino.api import dd, rt, _


def objects():

    Category = rt.models.products.Category
    Author = rt.models.products.Author
    UploadType = rt.models.uploads.UploadType

    kw = dict()
    kw.update(wanted=True)
    kw.update(dd.str2kw('name', _("Photo")))
    yield UploadType(**kw)

    furniture_cat = Category(
        product_type=ProductTypes.furniture, **dd.str2kw('name', _("Furniture")))
    yield furniture_cat
    thriller_cat = Category(
        product_type=ProductTypes.books, **dd.str2kw('name', _("Thriller")))
    yield thriller_cat

    for name in """\
Biographies
Business
Culture
Children
Medicine
""".splitlines():
        yield Category(product_type=ProductTypes.books, **dd.str2kw('name', name))


    def furniture(sales_price, name, **kwargs):
        kwargs = dd.str2kw('name', name, **kwargs)
        kwargs.update(category=furniture_cat)
        kwargs.update(sales_price=sales_price)
        return rt.models.products.Thing(**kwargs)

    def thriller(sales_price, title, author, **kwargs):
        author_obj, created = rt.models.products.Author.objects.get_or_create(**parse_name(author))
        if created:
            author_obj.full_clean()
            author_obj.save()
        kwargs = dd.str2kw('name', title, **kwargs)
        kwargs.update(category=thriller_cat)
        kwargs.update(sales_price=sales_price)
        kwargs.update(author=author_obj)
        kwargs.update(vat_class="reduced")
        drv = dd.plugins.products.barcode_driver
        if drv is not None:
            kwargs.update(barcode=drv.pop_demo_value())
        return rt.models.products.Book(**kwargs)

    yield furniture("199.99", _("Wooden table"))
    yield furniture("99.99", _("Wooden chair"))
    yield furniture("129.99", _("Metal table"))
    yield furniture("79.99", _("Metal chair"))
    yield thriller("9.95", "Eye of the Needle", "Ken Follett")
    yield thriller("9.95", "And then there were None", "Agatha Christie",
        body="""<i><b>And Then There Were None</b></i> is a <a
      href="https://en.wikipedia.org/wiki/Mystery_fiction"
      title="Mystery fiction">mystery novel</a> by the English writer <a
      href="https://en.wikipedia.org/wiki/Agatha_Christie" title="Agatha
      Christie">Agatha Christie</a>, described by her as the most
    difficult of her books to write.<sup
      id="cite_ref-ChristieLimited_2-0" class="reference"><a
href="https://en.wikipedia.org/wiki/And_Then_There_Were_None#cite_note-ChristieLimited-2">[2]</a></sup>
    It was first published in the United Kingdom by the <a
      href="https://en.wikipedia.org/wiki/Collins_Crime_Club"
      title="Collins Crime Club">Collins Crime Club</a> on 6 November
    1939, as <i><b>Ten Little Niggers</b></i>,<sup
      id="cite_ref-vuyqxh_3-0" class="reference"><a
href="https://en.wikipedia.org/wiki/And_Then_There_Were_None#cite_note-vuyqxh-3">[3]</a></sup>
    after the children's counting rhyme and <a
href="https://en.wikipedia.org/wiki/Ten_Little_Indians#Derivative_songs_and_books"
      title="Ten Little Indians">minstrel song</a>, which serves as a
    major element of the plot.<i><sup id="cite_ref-CC_4-0"
        class="reference"><a
href="https://en.wikipedia.org/wiki/And_Then_There_Were_None#cite_note-CC-4">[4]</a></sup><sup
        id="cite_ref-pendergast_5-0" class="reference"><a
href="https://en.wikipedia.org/wiki/And_Then_There_Were_None#cite_note-pendergast-5">[5]</a></sup>
    </i>
    (Source: <a href="https://en.wikipedia.org/wiki/And_Then_There_Were_None">Wikipedia</a>)

        """)
    yield thriller("9.95", "Murder on the Orient Express (Hercule Poirot #10)", "Agatha Christie")
