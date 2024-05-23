# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from udala.zinema.content.pelikula_container import IPelikulaContainer  # NOQA E501
from udala.zinema.testing import UDALA_ZINEMA_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PelikulaContainerIntegrationTest(unittest.TestCase):

    layer = UDALA_ZINEMA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_pelikula_container_schema(self):
        fti = queryUtility(IDexterityFTI, name='PelikulaContainer')
        schema = fti.lookupSchema()
        self.assertEqual(IPelikulaContainer, schema)

    def test_ct_pelikula_container_fti(self):
        fti = queryUtility(IDexterityFTI, name='PelikulaContainer')
        self.assertTrue(fti)

    def test_ct_pelikula_container_factory(self):
        fti = queryUtility(IDexterityFTI, name='PelikulaContainer')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPelikulaContainer.providedBy(obj),
            u'IPelikulaContainer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_pelikula_container_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='PelikulaContainer',
            id='pelikula_container',
        )

        self.assertTrue(
            IPelikulaContainer.providedBy(obj),
            u'IPelikulaContainer not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('pelikula_container', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('pelikula_container', parent.objectIds())

    def test_ct_pelikula_container_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PelikulaContainer')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_pelikula_container_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PelikulaContainer')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'pelikula_container_id',
            title='PelikulaContainer container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
