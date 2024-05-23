# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s udala.zinema -t test_pelikula_container.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src udala.zinema.testing.UDALA_ZINEMA_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/udala/zinema/tests/robot/test_pelikula_container.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a PelikulaContainer
  Given a logged-in site administrator
    and an add PelikulaContainer form
   When I type 'My PelikulaContainer' into the title field
    and I submit the form
   Then a PelikulaContainer with the title 'My PelikulaContainer' has been created

Scenario: As a site administrator I can view a PelikulaContainer
  Given a logged-in site administrator
    and a PelikulaContainer 'My PelikulaContainer'
   When I go to the PelikulaContainer view
   Then I can see the PelikulaContainer title 'My PelikulaContainer'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PelikulaContainer form
  Go To  ${PLONE_URL}/++add++PelikulaContainer

a PelikulaContainer 'My PelikulaContainer'
  Create content  type=PelikulaContainer  id=my-pelikula_container  title=My PelikulaContainer

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PelikulaContainer view
  Go To  ${PLONE_URL}/my-pelikula_container
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PelikulaContainer with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PelikulaContainer title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
