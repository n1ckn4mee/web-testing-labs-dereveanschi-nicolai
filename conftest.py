import os,json,time,tempfile
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from helpers import login
@pytest.fixture
def driver(request):
    options=webdriver.ChromeOptions()
    profiles=Path(os.environ.get('LAB_PROFILE_ROOT','profiles')).resolve();profiles.mkdir(parents=True,exist_ok=True)
    profile=profiles/Path.cwd().name;profile.mkdir(exist_ok=True)
    options.add_argument('--user-data-dir='+str(profile))
    options.add_argument('--window-size=1200,900')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    if os.environ.get('CI'):options.add_argument('--headless=new')
    if os.environ.get('LAB_CHROME_BINARY'):options.binary_location=os.environ['LAB_CHROME_BINARY']
    d=webdriver.Chrome(options=options,service=Service(os.environ['LAB_DRIVER_PATH'])) if os.environ.get('LAB_DRIVER_PATH') else webdriver.Chrome(options=options)
    d.delete_all_cookies()
    try:yield d
    finally:d.quit()
@pytest.fixture
def logged_in(driver):
    login(driver)
    return driver
