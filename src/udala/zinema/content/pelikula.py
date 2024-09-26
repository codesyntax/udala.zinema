# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.app.textfield import RichText
from plone.autoform.directives import widget

# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model
from udala.zinema import _

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from DateTime import DateTime
from plone.base.i18nl10n import weekdayname_msgid
from zope.i18n import translate
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from zope.interface import alsoProvides


class ISaioaRowSchema(Interface):
    eguna = schema.TextLine(title=_("Eguna"), default="AAAA/MM/DD")
    ordua = schema.TextLine(title=_("Ordua"), default="HH:MM")
    aretoa = schema.TextLine(title=_("Aretoa"))


class IPelikula(model.Schema):
    """Marker interface and Dexterity Python Schema for Pelikula"""

    ficha_tecnica = RichText(
        title=_("Ficha tecnica"),
        description=_("Ficha tecnica de la pelicula en catellano"),
        required=False,
    )

    fitxa_teknikoa = RichText(
        title=_("Fitxa teknikoa"),
        description=_("Pelikularen fitxa teknikoa euskaraz"),
        required=False,
    )

    trailer = schema.Text(
        title=_("Pelikularen trailerra"),
        description=_("Itsatsi hemen pelikularen trailerraren embed kodea"),
    )

    alt_text = schema.TextLine(
        title="Image alt text",
        description="Enter the alternative text for the image that will be read to invident users",
        required=False,
    )

    widget(saioak=DataGridFieldFactory)
    saioak = schema.List(
        title=_("Saioak"),
        value_type=DictRow(title=_("Saioak"), schema=ISaioaRowSchema),
        required=False,
    )


alsoProvides(IPelikula["ficha_tecnica"], ILanguageIndependentField)
alsoProvides(IPelikula["fitxa_teknikoa"], ILanguageIndependentField)
alsoProvides(IPelikula["trailer"], ILanguageIndependentField)
alsoProvides(IPelikula["alt_text"], ILanguageIndependentField)
alsoProvides(IPelikula["saioak"], ILanguageIndependentField)


@implementer(IPelikula)
class Pelikula(Container):
    """Content-type class for IPelikula"""

    def get_sorted_data(self):
        ret = {}
        for saioa in self.saioak:
            item = ret.get(saioa.get("eguna", ""), [])
            item.append(saioa.get("ordua", ""))
            ret[saioa.get("eguna", "")] = item
        return sorted(ret.items())

    def localized_dow(self, date):
        dt = DateTime(date, datefmt="international")
        dow = dt.dow()
        return translate(
            weekdayname_msgid(dow),
            target_language=self.Language(),
            domain="plonelocales",
        )

    def daynum(self, date):
        dt = DateTime(date, datefmt="international")
        return dt.day()
