from selenium import webdriver

'''
This program signs into your UW account and then tries to 
sign up for specified sln codes using a Chrome browser.
Download link for a chromium webdriver (https://chromedriver.chromium.org/)
'''

NET_ID = 'netid'
PASSWORD = 'netidpassword'
# your sln codes you wish to add
CSE_416_A = '12703'
CSE_416_AA = '12704'
CSE_416_AB = '12705'
CSE_416_AC = '12706'
CSE_416_AD = '12707'
CSE_492_J = '21580'

'''
2 status outcomes:
1. "Schedule not updated. Resolve errors listed below and resubmit."
2. "Schedule updated."
'''
def sign_up(course, section=None):
    driver = webdriver.Chrome()
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
    netid_element = driver.find_element_by_id('weblogin_netid')
    password_element = driver.find_element_by_id('weblogin_password')
    netid_element.send_keys(NET_ID)
    password_element.send_keys(PASSWORD)
    submit_button_element = driver.find_element_by_id('submit_button')
    submit_button_element.click()
    sln_box_element1 = driver.find_element_by_name("sln8")
    sln_box_element1.send_keys(course)
    if section != None:
        sln_box_element2 = driver.find_element_by_name("sln9")
        sln_box_element2.send_keys(section)
    update_schedule_button = driver.find_element_by_xpath('/html/body/div[@id="doneDiv"]/form/input[7]')
    update_schedule_button.click()
    status = driver.find_element_by_xpath('/html/body/div[@id="doneDiv"]/b')
    sln1_status = driver.find_element_by_xpath('/html/body/div[2]/form/p[2]/table/tbody/tr[2]/td[5]')
    sln2_status = driver.find_element_by_xpath('/html/body/div[2]/form/p[2]/table/tbody/tr[3]/td[5]')
    print(status.text)
    print(sln1_status.text)
    print(sln2_status.text)
    driver.quit()

    

sign_up(course=CSE_416_A,section=CSE_416_AC)
#sign_up(course=CSE_416_A,section=CSE_416_AD)
#sign_up(course=CSE_492_J)


