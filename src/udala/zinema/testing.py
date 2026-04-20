from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import udala.zinema


class UdalaZinemaLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)

        import collective.z3cform.datagridfield
        self.loadZCML(package=collective.z3cform.datagridfield)

        self.loadZCML(package=udala.zinema)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "udala.zinema:default")


UDALA_ZINEMA_FIXTURE = UdalaZinemaLayer()


UDALA_ZINEMA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UDALA_ZINEMA_FIXTURE,),
    name="UdalaZinemaLayer:IntegrationTesting",
)


UDALA_ZINEMA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UDALA_ZINEMA_FIXTURE,),
    name="UdalaZinemaLayer:FunctionalTesting",
)


UDALA_ZINEMA_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        UDALA_ZINEMA_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="UdalaZinemaLayer:AcceptanceTesting",
)
