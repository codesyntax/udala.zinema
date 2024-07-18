# -*- coding: utf-8 -*-

# from udala.zinema import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPelikulaContainerView(Interface):
    """ Marker Interface for IPelikulaContainerView"""


@implementer(IPelikulaContainerView)
class PelikulaContainerView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('pelikula_container_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
