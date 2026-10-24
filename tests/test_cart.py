import pytest
from helpers import *
@pytest.mark.smoke
def test_cart_add(logged_in):
    d=logged_in;w=WebDriverWait(d,10)
    w.until(EC.element_to_be_clickable((By.ID,'add-to-cart-sauce-labs-backpack'))).click()
    badge=w.until(EC.visibility_of_element_located((By.CLASS_NAME,'shopping_cart_badge'))).text
    assert badge=='1';record(d,'suite-cart-add',badge=badge)
@pytest.mark.regression
def test_cart_two_items(logged_in):
    d=logged_in;w=WebDriverWait(d,10)
    for item in ['sauce-labs-backpack','sauce-labs-bike-light']:
        w.until(EC.element_to_be_clickable((By.ID,'add-to-cart-'+item))).click()
        w.until(EC.visibility_of_element_located((By.CLASS_NAME,'shopping_cart_badge')))
    w.until(EC.text_to_be_present_in_element((By.CLASS_NAME,'shopping_cart_badge'),'2'))
    d.find_element(By.CLASS_NAME,'shopping_cart_link').click()
    w.until(EC.visibility_of_element_located((By.CLASS_NAME,'cart_item')))
    assert len(d.find_elements(By.CLASS_NAME,'cart_item'))==2
    d.find_element(By.ID,'checkout').click();w.until(EC.visibility_of_element_located((By.ID,'first-name')))
    fill(d,'Ion','Pop','3100');w.until(EC.url_contains('checkout-step-two'))
    names=[e.text for e in d.find_elements(By.CLASS_NAME,'inventory_item_name')]
    assert names==['Sauce Labs Backpack','Sauce Labs Bike Light']
    record(d,'suite-two-items',items=names)
