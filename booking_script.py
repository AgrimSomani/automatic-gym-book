from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from anticaptchaofficial.recaptchav2proxyless import *
from dotenv import load_dotenv
import os

load_dotenv()

def is_option_enabled(option_element):
    return not option_element.get_attribute('disabled')

def select_date(date:int,date_field):
    try:
        select = Select(date_field)
        select.select_by_index(date-1)
        return True
    except:
        print('Cannot book for that date yet.')
        return False

def get_fields(driver):
    name_field = driver.find_element(By.ID,'FirstName')
    email_field = driver.find_element(By.ID,'Email')
    uid_field = driver.find_element(By.ID,'MemberID')
    date_field = driver.find_element(By.ID,'DateList')
    time_field =  driver.find_element(By.ID,'SessionTime')
    center_field =  driver.find_element(By.ID,'CenterID')
    declare_field =  driver.find_element(By.ID,'dataCollection')
    submit_button = driver.find_element(By.ID,'sbmtBtn')

    return name_field,email_field,uid_field,date_field,time_field,center_field,declare_field,submit_button

def get_site_key(driver):
    site_key = driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
    return site_key

def set_user_info(name_field,email_field,uid_field,name,email, uid):
    name_field.send_keys(name)
    email_field.send_keys(email)
    uid_field.send_keys(uid)

def select_time(time_field,time_to_book):
    option_elements = time_field.find_elements(By.TAG_NAME, 'option')
    time_mapping = {
        1: '1700',  # Adjust the actual times as needed
        2: '1845',
        3: '2030'
    }
    for option in option_elements:
        if option.text.startswith(time_mapping[time_to_book]) and is_option_enabled(option):
            option.click()
            return True
    return False

# def transcribe(url):
#     with open('.temp', 'wb') as f:
#         f.write(requests.get(url).content)
#     # audio_file= open(".temp", "")

#     # transcript = openai.Audio.transcribe("whisper-1", audio_file)
#     # print(transcript["text"].strip())
#     # return transcript["text"].strip()

# def solve_audio_captcha(driver):
#     text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
#     driver.find_element(By.ID, "audio-response").send_keys(text)
#     driver.find_element(By.ID, "recaptcha-verify-button").click()

def recaptcha_handler(driver,solver):
    site_key = get_site_key(driver)
    solver.set_website_key(site_key)
    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print("g-response: "+g_response)
        input = driver.find_element(By.ID,'g-recaptcha-response')
        driver.execute_script("arguments[0].style.display = '';", input)
        driver.execute_script("arguments[0].innerHTML = arguments[1];", input,g_response)
        time.sleep(2.5)
        driver.execute_script("arguments[0].style.display ='none';", input)
        time.sleep(2)
    else:
        print("task finished with error "+solver.error_code)
        return False
    return True

    # span_inside_iframe = driver.find_element(By.CSS_SELECTOR, 'span.recaptcha-checkbox')
    # span_inside_iframe.click()
    # time.sleep(1.5)
    # driver.switch_to.default_content()
    # driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, f'iframe[title="recaptcha challenge expires in two minutes"]'))
    # driver.find_element(By.ID, "recaptcha-audio-button").click()
    # time.sleep(5)
    # solve_audio_captcha(driver)
    # driver.switch_to.default_content() 

def recaptcha_wrong(driver,home_url):
    current_url = driver.current_url
    print(current_url)
    print(home_url)
    return current_url == home_url

def confirm_data_privacy_handler(declare_field,driver):
    driver.execute_script("arguments[0].style.pointerEvents = 'auto';", declare_field)
    declare_field.click()

def main(name,email,uid,date,time_to_book):

    url = 'https://fcbooking.cse.hku.hk/Form/SignUpPS?CenterID=10002&Date=2023%2F08%2F21&HourID=10125'

    driver = webdriver.Chrome()
    driver.get(url)
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(os.getenv('SOLVER_KEY'))
    solver.set_website_url(url)
    
    while True:
        time.sleep(2)
        name_field,email_field,uid_field,date_field,time_field,center_field,declare_field,submit_button = get_fields(driver)

        if not select_date(date,date_field):
            return

        if select_time(time_field,time_to_book):
            set_user_info(name_field,email_field,uid_field,name,email,uid)
            time.sleep(3)
            confirm_data_privacy_handler(declare_field,driver)
            time.sleep(3)
            if recaptcha_handler(driver,solver):
                time.sleep(1)
                submit_button.click()
                if not recaptcha_wrong(driver,url):
                    return
            driver.refresh()
        else:
            time.sleep(10)
            driver.refresh()

if __name__ == "__main__":
    import sys
    
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 7:
        print(f"Usage: python booking_script.py <name> <email> <uid> <date> <time>, {7-len(sys.argv)} arguments not provided!")
    elif len(sys.argv) > 7:
        print(f"Usage: python booking_script.py <name> <email> <uid> <date> <time>, {len(sys.argv)-7} extra arguments provided!")
    else:
        name = sys.argv[2]
        email = sys.argv[3]
        uid = sys.argv[4]
        date_str = int(sys.argv[5])
        time_int = int(sys.argv[6])
        main(name, email, uid, date_str, time_int)






