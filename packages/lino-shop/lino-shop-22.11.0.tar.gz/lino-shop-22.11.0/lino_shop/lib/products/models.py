# -*- coding: UTF-8 -*-
# Copyright 2013-2022 Rumma & Ko Ltd

from django.conf import settings
from etgen.html import tostring

from lino.api import _
from lino_xl.lib.products.models import *
from lino_xl.lib.products.roles import ProductsStaff
from lino.mixins.human import Human
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.publisher.mixins import Publishable
from lino.modlib.publisher.choicelists import PublisherViews

from lino_shop.lib.shop.user_types import UserTypes

ProductTypes.clear()
add = ProductTypes.add_item
add('200', _("Furniture"), 'furniture', table_name="products.Furniture")
add('300', _("Books"), 'books', table_name="products.Books")
add('400', _("Things"), 'things', table_name="products.Things")
add('900', _("Services"), 'default', table_name="products.Products")



class ProductColors(dd.ChoiceList):
    # originally copied from cal.DisplayColors
    verbose_name = _("Product color")
    verbose_name_plural = _("Product colors")
    required_roles = dd.login_required(dd.SiteStaff)
add = ProductColors.add_item
names = 'White Silver Gray Black Red Maroon Yellow Olive Lime Green Aqua Teal Blue Navy Fuchsia Purple'
for color in names.split():
    add(color, _(color),color)


class BookTypes(dd.ChoiceList):
    verbose_name = _("Book type")
    verbose_name_plural = _("Book types")
    required_roles = dd.login_required(dd.SiteStaff)
add = BookTypes.add_item
add("010", _("Paperback"))
add("020", _("Hard cover"))
add("030", _("eBook"))
add("040", _("Audio"))


class Colored(dd.Model):
    class Meta(Product.Meta):
        app_label = 'products'
        abstract = True

    color = ProductColors.field(blank=True)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Colored, cls).get_simple_parameters():
            yield p
        yield "color"

class Product(Product, Publishable):
    # NB we probably won't be using publisher, but leave the hook here just in
    # case

    class Meta(Product.Meta):
        # verbose_name = _("Product")
        # verbose_name_plural = _("Product")
        abstract = dd.is_abstract_model(__name__, 'Product')

    # publisher_location = 'prod'
    publisher_page_template = "products/Product/page.pub.html"
    # publisher_item_template = "products/Product/item.pub.html"

    @dd.htmlbox()
    def full_page(self, ar):
        if ar is None:
            return ''
        return "".join(self.as_page(ar))

    def get_overview_elems(self, ar):
        # return [ar.obj2html(self)]
        yield self.obj2href(ar)
        yield self.get_full_preview(ar)
        # yield "Yes it's a product"
        for mf in rt.models.albums.UsagesByController.request(self):
            yield str(mf)

    def as_paragraph(self, ar):
        s = "<b>{}</b> : ".format(self)
        s += self.body_short_preview or "(no description)"
        s += "<br><b>{} {}</b>".format(self.sales_price, dd.plugins.ledger.currency_symbol)
        return s

    def as_page(self, ar):

        # print("20220927 as_page", self.id, self)
        yield "<h1>{}</h1>".format(self)
        yield self.body_full_preview
        yield "Price: {} {}".format(self.sales_price, dd.plugins.ledger.currency_symbol)
        if self.category is not None:
            yield "<p>Category: "
            yield tostring(self.category.obj2href(ar))
            yield "</p>"


        # tplname = "products/Product/full_page.html"
        # env = settings.SITE.plugins.jinja.renderer.jinja_env
        # context = ar.get_printable_context(obj=self)
        # template = env.get_template(tplname)
        # # print("20210112 publish {} {} using {}".format(cls, obj, template))
        # # context = dict(obj=self, request=request, language=get_language())
        # yield template.render(**context)

    @classmethod
    def get_dashboard_objects(cls, ar):
        qs = cls.objects.all()[0:3]
        # print("20220927", qs)
        return qs





# Product.set_widget_options('overview', verbose_name=None)
dd.update_field(Product, 'overview', verbose_name=None)


class Author(Human):
    class Meta:
        app_label = 'products'
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        abstract = dd.is_abstract_model(__name__, 'Author')



class Thing(Product, Colored):

    class Meta(Product.Meta):
        verbose_name = _("Thing")
        verbose_name_plural = _("Things")
        abstract = dd.is_abstract_model(__name__, 'Thing')

    # publisher_location = 'things'

    def as_paragraph(self, ar):
        s = "<b>{}</b> : ".format(self)
        if self.color:
            s += " " + str(self.color)
        s += self.body_short_preview or "(no description)"
        s += "<br><b>{} {}</b>".format(self.sales_price, dd.plugins.ledger.currency_symbol)
        return s

class Book(Product, UploadController):
    class Meta(Product.Meta):
        # app_label = 'products'
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        abstract = dd.is_abstract_model(__name__, 'Book')

    # publisher_location = 'books'

    isbn = models.CharField(_("ISBN"), max_length=255, blank=True)
    author = dd.ForeignKey('products.Author', blank=True, null=True)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Book, cls).get_simple_parameters():
            yield p
        yield "isbn"
        yield "author"

    def as_paragraph(self, ar):
        title = str(self)
        if self.author:
            title = str(self.author) + ": " + title
        # s = "<b>{}: {}</b> : ".format(self.author, self)
        s = "xx <b>{}</b> : ".format(title)
        s += self.body_short_preview or "(no description)"
        s += "<br><b>{} {}</b>".format(self.sales_price, dd.plugins.ledger.currency_symbol)
        return s


class ProductDetail(ProductDetail):

    main = "preview general sales misc"

    general = dd.Panel("""
    name
    id product_type category delivery_unit
    body
    """, _("General"), required_roles=dd.login_required(ProductsStaff))

    sales = dd.Panel("""
    sales_price vat_class sales_account
    sales.InvoiceItemsByProduct
    """, _("Sales"), required_roles=dd.login_required(ProductsStaff))

    preview = dd.Panel("""
    full_page
    """, _("Overview"))

    misc = dd.Panel("""
    barcode barcode_svg
    albums.UsagesByController
    """, _("Miscellaneous"), required_roles=dd.login_required(ProductsStaff))

class ThingDetail(ProductDetail):

    general = dd.Panel("""
    name color
    id product_type category delivery_unit
    body
    """, _("General"), required_roles=dd.login_required(ProductsStaff))


class BookDetail(ProductDetail):
    general = dd.Panel("""
    name author isbn
    id product_type category delivery_unit
    body
    """, _("General"), required_roles=dd.login_required(ProductsStaff))


# class Products(Products):


class Things(Products):
    model = 'products.Thing'
    detail_layout = "products.ThingDetail"
    _product_type = ProductTypes.things
    params_layout = "color category"
    column_names = "id name category color *"


class Furniture(Things):
    _product_type = ProductTypes.furniture


class Books(Products):
    model = 'products.Book'
    detail_layout = "products.BookDetail"
    _product_type = ProductTypes.books


class Authors(dd.Table):
    required_roles = dd.login_required(ProductsUser)
    model = "products.Author"

PublisherViews.add_item_lazy("prod", Products)
PublisherViews.add_item_lazy("things", Things)
PublisherViews.add_item_lazy("books", Books)
PublisherViews.add_item_lazy("furn", Furniture)
