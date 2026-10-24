import pytest
from helpers import *
@pytest.mark.smoke
def test_full_order(driver):
    d=driver;w=login(d)
    record(d,'products')
    if os.environ.get('LAB_ORDER_STAGE')=='skeleton':return
    w.until(EC.element_to_be_clickable((By.ID,'add-to-cart-sauce-labs-backpack'))).click()
    w.until(EC.visibility_of_element_located((By.CLASS_NAME,'shopping_cart_badge')))
    badge=d.find_element(By.CLASS_NAME,'shopping_cart_badge').text
    assert badge==('2' if os.environ.get('LAB_BREAK_ORDER') else '1')
    record(d,'cart-badge',badge=badge)
    if os.environ.get('LAB_ORDER_STAGE')=='add':return
    d.find_element(By.CLASS_NAME,'shopping_cart_link').click()
    name=w.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.inventory_item_name'))).text
    assert name=='Sauce Labs Backpack';record(d,'cart-item',item=name)
    d.find_element(By.ID,'checkout').click();w.until(EC.visibility_of_element_located((By.ID,'first-name')))
    fill(d,'Ion','Popescu','3100');w.until(EC.url_contains('checkout-step-two'))
    assert w.until(EC.visibility_of_element_located((By.CLASS_NAME,'title'))).text=='Checkout: Overview'
    total=d.find_element(By.CLASS_NAME,'summary_total_label').text;assert total.startswith('Total')
    record(d,'order-overview',total=total)
    if os.environ.get('LAB_ORDER_STAGE')=='overview':return
    w.until(EC.element_to_be_clickable((By.ID,'finish'))).click()
    header=w.until(EC.visibility_of_element_located((By.CLASS_NAME,'complete-header'))).text
    assert header=='Thank you for your order!'
    assert d.find_elements(By.CLASS_NAME,'shopping_cart_badge')==[]
    record(d,'order-complete',message=header,total=total)
