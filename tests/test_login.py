import pytest
from helpers import *
@pytest.mark.smoke
def test_login_valid(driver):
    w=login(driver)
    assert driver.find_element(By.CLASS_NAME,'title').text=='Products'
    record(driver,'suite-login')
@pytest.mark.regression
def test_locked_user(driver):
    w=login(driver,'locked_out_user')
    e=w.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h3[data-test='error']")))
    assert 'locked out' in e.text
    record(driver,'suite-locked',message=e.text)
@pytest.mark.regression
def test_invalid_password(driver):
    w=login(driver,valid=False)
    e=w.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h3[data-test='error']")))
    assert 'do not match' in e.text
    record(driver,'suite-invalid',message=e.text)
