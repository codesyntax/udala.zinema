# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.base.i18nl10n import weekdayname_msgid
from Products.Five.browser import BrowserView
from zope.i18n import translate


class PelikulaView(BrowserView):

    def saioak(self):
        return sorted(
            self.context.saioak,
            key=lambda x: DateTime(x["eguna"] + " " + x["ordua"], fmt="international"),
        )

    def localized_dow(self, date):
        dt = DateTime(date, datefmt="international")
        dow = dt.dow()
        return translate(
            weekdayname_msgid(dow),
            target_language=self.context.Language(),
            domain="plonelocales",
        )

    def daynum(self, date):
        dt = DateTime(date, datefmt="international")
        return dt.day()


class PelikulaImageForEvent(BrowserView):
    pass


class PelikulaForEvent(BrowserView):

    def saioak(self):

        return sorted(
            self.context.saioak,
            key=lambda x: DateTime(x["eguna"] + " " + x["ordua"], fmt="international"),
        )

    def localized_dow(self, date):
        dt = DateTime(date, datefmt="international")
        dow = dt.dow()
        return translate(
            weekdayname_msgid(dow),
            target_language=self.context.Language(),
            domain="plonelocales",
        )

    def daynum(self, date):
        dt = DateTime(date, datefmt="international")
        return dt.day()
