from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from udala.zinema import _
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implementer


class IPelikulaContainer(model.Schema):
    """Marker interface and Dexterity Python Schema for PelikulaContainer"""

    initial_stuff = RichText(
        title=_("Hitzorduaren hasierako testua"),
        description=_(
            "Karpeta honen helburua atari nagusiko asteburuko zinema karteldegiaren "
            "erakusgunearen maketazio txukun bat edukitzea da. Informazio orokorra "
            "dago bertan, hala nola, txartel salmentaren ordutegia eta informazio "
            "gehiago lortzeko telefonoa."
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

    show_warning = schema.Bool(
        title=_(
            "Oharra erakutsi?",
        ),
        description=_(
            "Aktibatuta badago, beheko oharra "
            "erakutsiko da zinema karteldegiaren atalean."
        ),
        required=False,
        default=False,
        readonly=False,
    )

    # Make sure to import: from plone.app.textfield import RichText
    warning = RichText(
        title=_(
            "Oharra",
        ),
        description="",
        default="",
        required=False,
        readonly=False,
    )


alsoProvides(IPelikulaContainer["show_warning"], ILanguageIndependentField)


@implementer(IPelikulaContainer)
class PelikulaContainer(Container):
    """Content-type class for IPelikulaContainer"""
