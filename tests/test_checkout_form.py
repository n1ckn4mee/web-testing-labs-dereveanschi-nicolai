import csv,pytest,os
from pathlib import Path
from helpers import *
users=list(csv.DictReader((Path(__file__).parents[1]/'data/users.csv').open(encoding='utf8')))
@pytest.mark.regression
@pytest.mark.parametrize('user',users,ids=['user-'+str(i+1) for i in range(10)])
def test_checkout_form(driver,user,request):
    w=login_add(driver);fill(driver,user['first_name'],user['last_name'],user['postcode'])
    w.until(EC.url_contains('checkout-step-two'))
    actual=w.until(EC.visibility_of_element_located((By.CLASS_NAME,'title'))).text
    expected='Broken expectation' if os.environ.get('LAB_BREAK_SUITE') and request.node.callspec.id=='user-1' else 'Checkout: Overview'
    assert actual==expected
    record(driver,'suite-form',dataset=request.node.callspec.id)
