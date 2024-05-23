# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from udala.zinema.content.pelikula import IPelikula  # NOQA E501
from udala.zinema.testing import UDALA_ZINEMA_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PelikulaIntegrationTest(unittest.TestCase):

    layer = UDALA_ZINEMA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_pelikula_schema(self):
        fti = queryUtility(IDexterityFTI, name='Pelikula')
        schema = fti.lookupSchema()
        self.assertEqual(IPelikula, schema)

    def test_ct_pelikula_fti(self):
        fti = queryUtility(IDexterityFTI, name='Pelikula')
        self.assertTrue(fti)

    def test_ct_pelikula_factory(self):
        fti = queryUtility(IDexterityFTI, name='Pelikula')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPelikula.providedBy(obj),
            u'IPelikula not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_pelikula_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Pelikula',
            id='pelikula',
        )

        self.assertTrue(
            IPelikula.providedBy(obj),
            u'IPelikula not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('pelikula', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('pelikula', parent.objectIds())

    def test_ct_pelikula_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Pelikula')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_pelikula_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Pelikula')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'pelikula_id',
            title='Pelikula container',
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
