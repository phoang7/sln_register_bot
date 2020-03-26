import imaplib
import email
from selenium import webdriver

'''
This program logins into an email that receives Notify.UW emails
and reads emails that contain such emails. If it does receive an Notify.UW email,
it reads the subject and acts based on the course that is in the notification.
It grabs that course's sln code and attempts to sign up for that class using
a Chrome browser by sigining into your UW account.
This program stops running when it successfully signs up.
'''

SUCCESS = 'Schedule updated.'
FAIL = 'Schedule not updated. Resolve errors listed below and resubmit.'
NET_ID = 'yournetid'
PASSWORD = 'yournetidpassword'
# classes/sln codes you want to register for
CSE_416_A = '12703'
CSE_416_AA = '12704'
CSE_416_AB = '12705'
CSE_416_AC = '12706'
CSE_416_AD = '12707'
CSE_492_J = '21580'
registered = False
'''
This is the email that only receives notify.uw emails.
You can assign the email to receive notifications here:
https://notify.uw.edu/
'''
email_username = "youremailaddress"
email_password = "youremailpassword"

'''
Launches chrome (need to have webdriver installed).
The webdriver for chrome can be downloaded here:
https://sites.google.com/a/chromium.org/chromedriver/downloads
Once chrome is launched, logins into uw account to go access
"Register using SLN codes" and inserts sln codes passed into the
method.
lecture = sln code (lecture section) you want to sign up for
section = sln code (quiz section) you want to sign up for
'''
def sign_up(lecture, section=None):
    driver = webdriver.Chrome()
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
    netid_element = driver.find_element_by_id('weblogin_netid')
    password_element = driver.find_element_by_id('weblogin_password')
    netid_element.send_keys(NET_ID)
    password_element.send_keys(PASSWORD)
    submit_button_element = driver.find_element_by_id('submit_button')
    submit_button_element.click()
    sln_box_element1 = driver.find_element_by_name("sln8")
    sln_box_element1.send_keys(lecture)
    # if section != None:
    sln_box_element2 = driver.find_element_by_name("sln9")
    sln_box_element2.send_keys(section)
    update_schedule_button = driver.find_element_by_xpath('/html/body/div[@id="doneDiv"]/form/input[7]')
    update_schedule_button.click()
    

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

mail.login(email_username, email_password)


print('Registering for classes...')

'''
This loop waits to receive an email from Notify.UW, if so it then attempts
to sign up for the class from the received email. If fails, then loops keep
running. Only stops if the sign up is successful
'''
while not registered:
    
    print("getting inbox...")
    mail.select('Inbox')
    search_result, data = mail.uid('search', None, 'All')

    # print(data)
    inbox_item_list = data[0].split()
    # print(inbox_item_list)

    for item in inbox_item_list:
        fetch_result, email_data = mail.uid('fetch', item, '(RFC822)')

        raw_email = email_data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        subject = email_message['Subject']
        notify_uw = subject.startswith('Notify.UW')
        section = None
        if notify_uw:
            if  'cse 416 ac' in subject:
                sign_up(lecture=CSE_416_A,section=CSE_416_AC)
                registered = True
            elif 'cse 416 ad' in subject:
                sign_up(lecture=CSE_416_A,section=CSE_416_AD)
                registered = True
            mail.uid("store", item, "X-GM-LABELS", "\\Trash")
