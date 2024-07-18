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


class ISaioaRowSchema(Interface):
    eguna = schema.TextLine(title=_(u"Eguna"), default="AAAA/MM/DD")
    ordua = schema.TextLine(title=_(u"Ordua"), default="HH:MM")
    aretoa = schema.TextLine(title=_(u"Aretoa"))

class IPelikula(model.Schema):
    """ Marker interface and Dexterity Python Schema for Pelikula
    """
    ficha_tecnica = RichText(
        title=_(u'Ficha tecnica'),
        description=_("Ficha tecnica de la pelicula en catellano"),
        required=False
    )

    fitxa_teknikoa = RichText(
        title=_(u'Fitxa teknikoa'),
        description=_("Pelikularen fitxa teknikoa euskaraz"),
        required=False
    )

    trailer = schema.Text(
        title=_(u"Pelikularen trailerra"),
        description=_(u"Itsatsi hemen pelikularen trailerraren embed kodea")
        )

    alt_text = schema.TextLine(
        title=u"Image alt text",
        description=u"Enter the alternative text for the image that will be read to invident users",
        required=False,
    )

    widget(saioak=DataGridFieldFactory)
    saioak = schema.List(
        title=_(u"Saioak"),
        value_type=DictRow(title=_(u"Saioak"), schema=ISaioaRowSchema),
        required=False,
    )



@implementer(IPelikula)
class Pelikula(Container):
    """ Content-type class for IPelikula
    """
