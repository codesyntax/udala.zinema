# -*- coding: utf-8 -*-
from plone.app.textfield import RichText

# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model
from udala.zinema import _

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


class IPelikulaContainer(model.Schema):
    """Marker interface and Dexterity Python Schema for PelikulaContainer"""

    initial_stuff = RichText(
        title=_("Hitzorduaren hasierako testua"),
        description=_(
            "Testu orokor hau ebentuaren aurretik agertuko da eta bere helburua webgunearen maketazio txukun bat edukitzea da. Informazio orokorra dago bertan, hala nola, txartel salmentaren ordutegia eta informazio gehiago lortzeko telefonoa."
        ),
        required=False,
    )

    text = RichText(title=_("Programazioaren informazioa"), required=False)

    title_eu = schema.TextLine(title=_("Sortuko duen hitzorduaren titulua euskaraz"))

    title_es = schema.TextLine(title=_("Sortuko duen hitzorduaren titulua gazteleraz"))

    # subject_eu = schema.List(title=_(u"Sortuko duen hitzorduaren titulua euskaraz"))

    # subject_es = schema.List(title=_(u"Sortuko duen hitzorduaren titulua gazteleraz"))

    subject_eu = schema.List(
        title=_(
            "Sortuko den hitzorduaren etiketak euskaraz",
        ),
        description=_(
            "",
        ),
        value_type=schema.TextLine(
            title="",
        ),
        default=[],
        required=False,
        readonly=False,
    )

    subject_es = schema.List(
        title=_(
            "Sortuko den hitzorduaren etiketak gazteleraz",
        ),
        description=_(
            "",
        ),
        value_type=schema.TextLine(
            title="",
        ),
        default=[],
        required=False,
        readonly=False,
    )

    location_eu = schema.TextLine(title=_("Lekua euskaraz"))

    location_es = schema.TextLine(title=_("Lekua gazteleraz"))


@implementer(IPelikulaContainer)
class PelikulaContainer(Container):
    """Content-type class for IPelikulaContainer"""
