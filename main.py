import pyderman as driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

path = driver.install(browser=driver.chrome)
print(f"Installed chromedriver driver to path: {path}")
service = Service(executable_path=path)

# for now
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')

driver = webdriver.Chrome(service=service, options=options)
# actions = ActionChains(driver)

# userid: [siteid, sercurity groups, person groups, labor]
userids = {
    'GVXXMECH': ['GV', ['GV', 'Mech-Mobile', 'Mech'],  'Mech-MW'],
    'GVXXELEC': ['GV', ['GV', 'Mech-Mobile', 'Mech'],  'ELECT'],
    'GVXXPROD': ['GV', ['GV', 'PRODSUPER'],  ''],
    'GVXXPLAN': ['GV', ['GV', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'],  ''],
    'GVXXRENG': ['GV', ['GV', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'],  ''],
    'GVXXINVC': ['GV', ['GV', 'STOREROOM', 'VIEWER1'],  ''],
    'GVXXMNTS': ['GV', ['GV', 'MAINTSUPER', 'VIEWER1'],  ''],
    'GVXXPNTS': ['GV', ['GV', 'SUPERINT', 'VIEWER1'],  ''],
    'BAXXMECH': ['BA', ['BA', 'Mech-Mobile', 'Mech'],  'Mech-MW'],
    'BAXXELEC': ['BA', ['BA', 'Mech-Mobile', 'Mech'],  'ELECT'],
    'BAXXPROD': ['BA', ['BA', 'PRODSUPER'],  ''],
    'BAXXPLAN': ['BA', ['BA', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'],  ''],
    'BAXXRENG': ['BA', ['BA', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'],  ''],
    'BAXXINVC': ['BA', ['BA', 'STOREROOM', 'VIEWER1'],  ''],
    'BAXXMNTS': ['BA', ['BA', 'MAINTSUPER', 'VIEWER1'],  ''],
    'BAXXPNTS': ['BA', ['BA', 'SUPERINT', 'VIEWER1'],  ''],
    'ANTXMECH': ['ANT', ['ANT', 'Mech-Mobile', 'Mech', 'STOREROOM'],  'Mech-MW'],
    'ANTXUSER': ['ANT', ['ANT', 'MAINTSUPER', 'VIEWER1', 'MAXTECH','PLANNER', 'SCHEDULER', 'STOREROOM'],  ''],
    'ANTXINVC': ['ANT', ['ANT', 'STOREROOM', 'VIEWER1'],  '']
}

persongroups = {}


def ensureLoggedIn():
    isLoggedInAdmin = False
    driver.get(
        "https://admin.test.apps.iko-openshift-cluster.iko.max-it-eam.com/users"
    )

    while not (isLoggedInAdmin):
        try:
            login = WebDriverWait(driver, timeout=5).until(
                lambda d: d.find_element(By.ID, value="column-username"))
        except Exception as e:
            isLoggedInAdmin = False
            login = WebDriverWait(driver, timeout=5).until(
                lambda d: d.find_element(By.ID, value="username"))
            login.send_keys('majona')
            login.submit()

            # password
            login = WebDriverWait(driver, timeout=5).until(
                lambda d: d.find_element(By.ID, value="password"))
            login.send_keys('ClassroomIKO123')
            login.submit()
        else:
            isLoggedInAdmin = True
    return True


def createUsers(userid):
    ensureLoggedIn()
    driver.get(
        "https://admin.test.apps.iko-openshift-cluster.iko.max-it-eam.com/users/add"
    )
    # close the tour popup
    try:
        close = WebDriverWait(driver, timeout=2).until(
            lambda d: d.find_element(By.CLASS_NAME, 'walkme-x-button'))
        close.click()
    except Exception:
        pass
    # new_user = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, '//button[text()="Add user"]'))
    # new_user.click()

    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//input[@name="displayName"]'))
    field.send_keys(userid)
    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//input[@name="username"]'))
    field.send_keys(userid)
    field = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
        By.XPATH, '//input[@name="primaryEmail.value"]'))
    field.send_keys(f'{userid}@TEST.COM')
    # enable manual password
    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//a[text()="Enter manually"]'))
    field.click()
    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//input[@name="password"]'))
    field.send_keys('ClassroomIKO123')

    field = WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.ID, value="downshift-0-toggle-button"))
    # button must be in view to click
    driver.execute_script("arguments[0].scrollIntoView(true);", field)
    field.click()
    try:
        WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.ID, value="downshift-0-item-1")).click()
    except Exception:
        field.click()
        WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.ID, value="downshift-0-item-1")).click()

    save = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//button[text()="Create"]'))
    save.click()

    save = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Close"]')))
    driver.find_element(By.XPATH, '//button[text()="Close"]').click()

def updatePeople(userid, userdetails):
    ensureLoggedIn()
    driver.get(
        f"https://test.manage.test.apps.iko-openshift-cluster.iko.max-it-eam.com/maximo/oslc/graphite/manage-shell/index.html#/main?event=loadapp&value=person&additionalevent=useqbe&additionaleventvalue=PERSONID={userid}"
    )
    # first load can take > 10 seconds
    # the details are in an iframe...
    iframe = WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element(By.ID, 'manage-shell_Iframe'))
    driver.switch_to.frame(iframe)
    # calendar 
    field = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.ID, 'm955a6e44-tb')))
    field.click()
    field.send_keys(f'{userdetails[0]}M')
    # siteid
    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.ID, 'md3f7d577-tb'))
    driver.execute_script("arguments[0].scrollIntoView(true);", field)
    field.send_keys(userdetails[0])
    # save
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.ID, 'toolactions_SAVE-tbb_anchor')).click()


updatePeople('ANTXMECH', userids['ANTXMECH'])
print('end test')

for user in userids:
    createUsers(f'{user}1')

print('created users')

driver.quit()
