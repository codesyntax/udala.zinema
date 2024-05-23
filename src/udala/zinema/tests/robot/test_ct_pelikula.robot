# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s udala.zinema -t test_pelikula.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src udala.zinema.testing.UDALA_ZINEMA_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/udala/zinema/tests/robot/test_pelikula.robot
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

Scenario: As a site administrator I can add a Pelikula
  Given a logged-in site administrator
    and an add Pelikula form
   When I type 'My Pelikula' into the title field
    and I submit the form
   Then a Pelikula with the title 'My Pelikula' has been created

Scenario: As a site administrator I can view a Pelikula
  Given a logged-in site administrator
    and a Pelikula 'My Pelikula'
   When I go to the Pelikula view
   Then I can see the Pelikula title 'My Pelikula'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Pelikula form
  Go To  ${PLONE_URL}/++add++Pelikula

a Pelikula 'My Pelikula'
  Create content  type=Pelikula  id=my-pelikula  title=My Pelikula

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Pelikula view
  Go To  ${PLONE_URL}/my-pelikula
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Pelikula with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Pelikula title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
