# -*- coding: utf-8 -*-

from logging import getLogger

from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from plone import api
from plone.app.multilingual import api as pamapi
from plone.app.textfield import RichTextValue
from plone.base.utils import safe_text
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from udala.zinema import _
from udala.zinema.config import REFERENCED_FILM
from udala.zinema.content.pelikula_container import IPelikulaContainer
from udala.zinema.interfaces import IPelikulaEvent
from zExceptions import Forbidden
from zope.component import getMultiAdapter
from zope.interface import Interface, alsoProvides, implementer
from plone.event.interfaces import IEventAccessor


class IPelikulaContainerView(Interface):
    """Marker Interface for IPelikulaContainerView"""


@implementer(IPelikulaContainerView)
class PelikulaContainerView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('pelikula_container_view.pt')

    def editing_permission(self):
        pps = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        return not pps.anonymous()

    def get_latest_films(self, num=10):
        return self.context.getFolderContents(
            {
                "portal_type": "Pelikula",
                "sort_on": "created",
                "sort_order": "reverse",
            },
            full_objects=True,
        )[:num]


class CreatePelikulaEvents(BrowserView):

    def __call__(self):

        log = getLogger(__name__)
        context = aq_inner(self.context)
        if not self.request.get("translate", None):
            authenticator = getMultiAdapter(
                (context, self.request), name="authenticator"
            )
            if not authenticator.verify():
                raise Forbidden()

        contents = []

        for id in self.request.get("ids", []):
            item = self.context.get(id, None)
            if item is None:
                log.info("There is no item with id=%s", id)
            else:
                contents.append(item)

        if contents:
            self.event = self.create_event_with_pelikulas(contents)
        else:
            self.event = None

        if self.event is None:
            msg = _("Ezin izan da hitzordua sortu")
            tipo = "error"
            url = self.context.absolute_url()
        else:
            msg = _("Hitzordua ondo sortu ")
            tipo = "info"
            url = self.event.absolute_url()

        api.portal.show_message(message=msg, type=tipo)
        return self.request.response.redirect(url)

    def get_mezuak(self):
        context = aq_inner(self.context)
        MEZUAK = {}
        MEZUAK["title"] = {
            "eu": context.title_eu,
            "es": context.title_es,
        }

        MEZUAK["subject"] = {
            "eu": context.subject_eu,
            "es": context.subject_es,
        }

        MEZUAK["location"] = {
            "eu": context.location_eu,
            "es": context.location_es,
        }

        MEZUAK["translation"] = {
            "eu": "es",
            "es": "eu",
        }
        return MEZUAK

    def create_event_with_pelikulas(self, items):
        context = aq_inner(self.context)
        language = context.Language()
        MEZUAK = self.get_mezuak()
        title = self.compose_title(items, language)
        start_date = self.get_first_day(items)
        end_date = self.get_last_day(items)
        html_content = self.get_html_content(items)
        parent = aq_parent(aq_parent(context)).get("agenda", aq_parent(context))
        if language == "es":
            id = "cartelera-cine-fin-de-semana-%s" % start_date.strftime("%d-%m-%Y")
        else:
            id = "%s-asteburuko-zinema-karteldegia" % start_date.strftime("%Y-%m-%d")

        while id in parent.keys():
            id = id + "-1"

        event = api.content.create(
            container=parent,
            type="Event",
            title=title,
            text=RichTextValue(
                safe_text(self.get_initial_stuff(language).output)
                + safe_text(html_content)
            ),
            # start=start_date,
            # end=end_date,
            location=MEZUAK["location"][language],
            subjects=MEZUAK["subject"][language],
            eventUrl=context.absolute_url(),
        )
        IEventAccessor(event).start = start_date
        IEventAccessor(event).end = end_date

        alsoProvides(event, IPelikulaEvent)
        # Set the content of the container and add reference
        # to the films
        context.text = event.text

        api.relation.delete(source=context, relationship=REFERENCED_FILM)
        # context.deleteReferences(REFERENCED_FILM)
        for item in items:
            # context.addReference(item, REFERENCED_FILM)
            api.relation.create(
                source=context, target=item, relationship=REFERENCED_FILM
            )

        translated, trans_items = self.create_translated_event(event, items)
        # translated_context = context.getTranslation(MEZUAK["translation"][language])
        translation_manager = pamapi.get_translation_manager(context)
        translated_context = translation_manager.get_translation(
            MEZUAK["translation"][language]
        )
        # Set the content and references to translated content
        translated_context.text = translated.text

        # translated_context.deleteReferences(REFERENCED_FILM)
        api.relation.delete(source=translated_context, relationship=REFERENCED_FILM)
        for item in trans_items:
            # translated_context.addReference(item, REFERENCED_FILM)
            api.relation.create(
                source=translated_context, target=item, relationship=REFERENCED_FILM
            )

        return event

    def create_translated_event(self, event, items):
        MEZUAK = self.get_mezuak()
        target_language = MEZUAK["translation"][event.Language()]
        trans_items = []
        for item in items:
            manager = pamapi.get_translation_manager(item)

            try:
                # trans_items.append(item.addTranslation(target_language))
                manager.add_translation(target_language)
                translation = manager.get_translation(target_language)
                trans_items.append(translation)
            except Exception as e:
                from logging import getLogger

                log = getLogger(__name__)
                log.info("Item already translated: %s", item.Title())

                # trans_items.append(item.getTranslation(target_language))
                translation = manager.get_translation(target_language)
                trans_items.append(translation)

        title = self.compose_title(trans_items, target_language)

        html_content = self.get_html_content(trans_items)
        manager = pamapi.get_translation_manager(event)
        try:
            if target_language == "es":
                id = "cartelera-cine-fin-de-semana-%s" % event.start.strftime(
                    "%d-%m-%Y"
                )
            else:
                id = "%s-asteburuko-zinema-karteldegia" % event.end.strftime("%Y-%m-%d")

            parent_manager = pamapi.get_translation_manager(aq_parent(event))

            while id in parent_manager.get_translation(target_language).keys():
                id = id + "-1"

            manager.add_translation(target_language)
            trans_event = manager.get_translation(target_language)

            api.content.rename(obj=trans_event, new_id=id)
            trans_event.title = title
            trans_event.text = RichTextValue(
                self.get_initial_stuff(target_language).output + html_content
            )
            trans_event.location = MEZUAK["location"][target_language]
            trans_event.subjects = MEZUAK["subject"][target_language]
            trans_event.reindexObject()

            context_manager = pamapi.get_translation_manager(self.context)
            context_translation = context_manager.get_translation(target_language)
            trans_event.eventUrl = context_translation.absolute_url()
        except Exception as e:
            log.info("Error creating the translated event")
            log.exception(e)

            trans_event = manager.get_translation(target_language)

        alsoProvides(trans_event, IPelikulaEvent)
        return trans_event, trans_items

    def compose_title(self, items, language):
        MEZUAK = self.get_mezuak()
        return MEZUAK["title"][language]

    def get_first_day(self, items):
        dates = self.get_dates(items)
        dates.sort()
        date = dates[0]
        return date.earliestTime()

    def get_last_day(self, items):
        dates = self.get_dates(items)
        dates.sort()
        date = dates[-1]
        return date.latestTime()

    def get_dates(self, items):
        dates = []
        for item in items:
            for saioa in item.saioak:
                dates.append(DateTime(saioa["eguna"], fmt="international"))

        return dates

    def get_html_content(self, items):
        images = ""
        html = ""
        num = 0
        for item in items:

            images += self.get_top_image(item, num)
            html += self.get_content_for_pelikula(item, num)
            num = num + 1

        return images + "<br /> <br />" + html

    def get_top_image(self, item, num=0):
        self.request.set("num", num)

        return getMultiAdapter((item, self.request), name="pelikula-image-for-event")()

    def get_content_for_pelikula(self, item, num=0):
        if item.Language() != self.request.LANGUAGE:
            # We are creating the translation
            # so we need a new unpoluted request
            from zope.publisher.browser import TestRequest

            request = TestRequest(num=num)
        else:
            request = self.request
            request.set("num", num)
        view = getMultiAdapter((item, request), name="pelikula-for-event")
        return view()

    def get_initial_stuff(self, language):
        manager = pamapi.get_translation_manager(self.context)
        item = manager.get_translation(language)
        return item.initial_stuff
