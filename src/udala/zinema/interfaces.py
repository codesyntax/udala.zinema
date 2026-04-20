"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUdalaZinemaLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPelikulaEvent(Interface):
    """Marker interface to mark events of films"""
