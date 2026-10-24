import os,json,time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
URL='http://127.0.0.1:8010'
def record(d,stage,**data):
    path=Path('evidence');path.mkdir(exist_ok=True)
    name=stage+'-'+str(time.time_ns())
    d.save_screenshot(str(path/(name+'.png')))
    with Path('events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps({'stage':stage,'url':d.current_url,**data},ensure_ascii=False)+'\n')
def login(d,user='standard_user',valid=True):
    d.get(URL+'/')
    w=WebDriverWait(d,10)
    w.until(EC.visibility_of_element_located((By.ID,'user-name'))).send_keys(user)
    d.find_element(By.ID,'password').send_keys(os.environ['LAB_TEST_PASSWORD']+('' if valid else '-wrong'))
    d.find_element(By.ID,'login-button').click()
    if user=='standard_user' and valid:w.until(EC.url_contains('inventory.html'));w.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.title')))
    return w
def login_add(d):
    w=login(d)
    w.until(EC.element_to_be_clickable((By.ID,'add-to-cart-sauce-labs-backpack'))).click()
    w.until(EC.text_to_be_present_in_element((By.CLASS_NAME,'shopping_cart_badge'),'1'))
    d.find_element(By.CLASS_NAME,'shopping_cart_link').click()
    w.until(EC.element_to_be_clickable((By.ID,'checkout'))).click()
    w.until(EC.visibility_of_element_located((By.ID,'first-name')))
    return w
def fill(d,first,last,code):
    for key,value in [('first-name',first),('last-name',last),('postal-code',code)]:
        if value:d.find_element(By.ID,key).send_keys(value)
    record(d,'form-filled',first=first,last=last,postcode=code)
    d.find_element(By.ID,'continue').click()
