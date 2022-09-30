import pyderman as driver
import time
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

path = driver.install(browser=driver.chrome)
print(f"Installed chromedriver driver to path: {path}")
service = Service(executable_path=path)

# for now
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')

driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window()
# actions = ActionChains(driver)

# userid: [siteid, sercurity groups, person groups, labor, supervisor]
userids = {
    'GVXXMECH': ['GV', ['GV', 'MECH-MOBILE', 'MECH'], 'MECH-MW'],
    'GVXXELEC': ['GV', ['GV', 'MECH-MOBILE', 'MECH'], 'ELECT'],
    'GVXXPROD': ['GV', ['GV', 'PRODSUPER'], ''],
    'GVXXPLAN': [
        'GV',
        ['GV', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'], ''
    ],
    'GVXXRENG': [
        'GV',
        ['GV', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'], ''
    ],
    'GVXXINVC': ['GV', ['GV', 'STOREROOM', 'VIEWER1'], ''],
    'GVXXMNTS':
    ['GV', ['GV', 'MAINTSUPER-MOBILE', 'MAINTSUPER', 'VIEWER1'], ''],
    'GVXXPNTS': ['GV', ['GV', 'SUPERINT', 'VIEWER1'], ''],
    'BAXXMECH': ['BA', ['BA', 'MECH-MOBILE', 'MECH'], 'MECH-MW'],
    'BAXXELEC': ['BA', ['BA', 'MECH-MOBILE', 'MECH'], 'ELECT'],
    'BAXXPROD': ['BA', ['BA', 'PRODSUPER'], ''],
    'BAXXPLAN': [
        'BA',
        ['BA', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'], ''
    ],
    'BAXXRENG': [
        'BA',
        ['BA', 'MAXTECH', 'PLANNER', 'SCHEDULER', 'STOREROOM', 'VIEWER1'], ''
    ],
    'BAXXINVC': ['BA', ['BA', 'STOREROOM', 'VIEWER1'], ''],
    'BAXXMNTS':
    ['BA', ['BA', 'MAINTSUPER-MOBILE', 'MAINTSUPER', 'VIEWER1'], ''],
    'BAXXPNTS': ['BA', ['BA', 'SUPERINT', 'VIEWER1'], ''],
    'ANTXMECH':
    ['ANT', ['ANT', 'MECH-MOBILE', 'MECH', 'STOREROOM'], 'MECH-MW'],
    'ANTXUSER': [
        'ANT',
        [
            'ANT', 'MAINTSUPER-MOBILE', 'MAINTSUPER', 'VIEWER1', 'MAXTECH',
            'PLANNER', 'SCHEDULER', 'STOREROOM'
        ], ''
    ],
    'ANTXINVC': ['ANT', ['ANT', 'STOREROOM', 'VIEWER1'], '']
}

uploadFiles = {
    'IKO_PERGRP': 'persongroups.csv',
    'IKO_ITEMMASTER': 'IKO_ITEMMASTER',
    'IKO_LOCATION':'IKO_LOCATION',
    'IKO_ASSET':'IKO_ASSET',
    'IKO_JOBPLAN':'IKO_JOBPLAN',
    'IKO_JPASSETLINK': 'IKO_JPASSETLINK',
    'IKO_JOBLABOR': 'IKO_JOBLABOR'
}


def ensureLoggedIn():
    isLoggedInAdmin = False
    if (('auth' not in driver.current_url) and ('login' not in driver.current_url)):
        isLoggedInAdmin = True

    if ('iko.max-it-eam.com' not in driver.current_url):
        driver.get('https://admin.dev.iko.max-it-eam.com/users')
        isLoggedInAdmin = False

    while not (isLoggedInAdmin):
        try:
            login = WebDriverWait(driver, timeout=5).until(
                lambda d: d.find_element(By.ID, value="username"))
            login.send_keys('majona')
            login.submit()

            # password
            login = WebDriverWait(driver, timeout=5).until(
                lambda d: d.find_element(By.ID, value="password"))
            login.send_keys('maximo123456789')
            login.submit()
        except Exception:
            isLoggedInAdmin = False
        else:
            isLoggedInAdmin = True
    return True


def createUsers(userid):
    ensureLoggedIn()
    driver.get("https://admin.dev.iko.max-it-eam.com/users/add")
    # close the tour popup
    try:
        close = WebDriverWait(driver, timeout=2).until(
            lambda d: d.find_element(By.CLASS_NAME, 'walkme-x-button'))
        close.click()
    except Exception:
        pass

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
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(
            By.ID, value="downshift-0-item-1")).click()
    except Exception:
        field.click()
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(
            By.ID, value="downshift-0-item-1")).click()

    save = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, '//button[text()="Create"]'))
    save.click()

    save = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Close"]')))
    driver.find_element(By.XPATH, '//button[text()="Close"]').click()


def updatePeople(userid, userdetails):
    ensureLoggedIn()
    driver.get(
        f"https://dev.manage.dev.iko.max-it-eam.com/maximo/oslc/graphite/manage-shell/index.html#/main?event=loadapp&value=person&additionalevent=useqbe&additionaleventvalue=PERSONID={userid}"
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
    field = WebDriverWait(
        driver,
        timeout=10).until(lambda d: d.find_element(By.ID, 'md3f7d577-tb'))
    driver.execute_script("arguments[0].scrollIntoView(true);", field)
    field.send_keys(userdetails[0])
    # save
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
        By.ID, 'toolactions_SAVE-tbb_anchor')).click()


def updateUser(userid, userdetails):
    ensureLoggedIn()
    driver.get(
        f"https://dev.manage.dev.iko.max-it-eam.com/maximo/oslc/graphite/manage-shell/index.html#/main?event=loadapp&value=user&additionalevent=useqbe&additionaleventvalue=userid={userid}"
    )
    
    iframe = WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element(By.ID, 'manage-shell_Iframe'))
    driver.switch_to.frame(iframe)

    # default insert site
    field = WebDriverWait(
        driver,
        timeout=10).until(lambda d: d.find_element(By.ID, 'maf836c7d-tb'))
    driver.execute_script("arguments[0].scrollIntoView(true);", field)
    field = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.ID, 'maf836c7d-tb')))
    field.click()
    field.send_keys(userdetails[0])
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
        By.ID, 'toolactions_SAVE-tbb_anchor')).click()
    time.sleep(2)

    actions = ActionChains(driver)
    filepath = os.path.abspath('securitygroups.csv')
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['USERID', 'GROUPNAME'])
        for group in userdetails[1]:
            writer.writerow([userid, group])

    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
        By.ID, 'md86fe08f_ns_menu_IFIMPORT_OPTION')).click()
    field = WebDriverWait(
        driver,
        timeout=10).until(lambda d: d.find_element(By.ID, 'm5bd8376e-tb'))
    field.send_keys('IKO_GROUPUSER')
    actions.send_keys(Keys.TAB)
    # fuck another iframe wtf
    iframe2 = WebDriverWait(
        driver,
        timeout=20).until(lambda d: d.find_element(By.ID, 'upload_iframe'))
    driver.switch_to.frame(iframe2)
    field = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.XPATH, "//input[@type='file']"))
    field.send_keys(filepath)
    driver.switch_to.default_content()
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.ID, 'md0955453-pb')).click()
    time.sleep(5)

for user in userids:
    try:
        createUsers(user)
    except Exception:
        print(f'failed to create user {user}')

for user in userids:
    try:
        updatePeople(user, userids[user])
    except Exception:
        print(f'failed to update people {user}')

for user in userids:
    try:
        updateUser(user, userids[user])
    except Exception:
        print(f'failed to update user {user}')

print('complete')

driver.quit()
