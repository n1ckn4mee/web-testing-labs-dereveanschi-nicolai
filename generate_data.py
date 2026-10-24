import csv,hashlib,json
from pathlib import Path
from faker import Faker

def generate(locale):
    f=Faker(locale);f.seed_instance(1)
    return [{'first_name':f.first_name(),'last_name':f.last_name(),'email':f.safe_email(),'address':f.address(),'phone':f.phone_number(),'postcode':f.postcode()} for _ in range(10)]
if __name__=='__main__':
    Path('data').mkdir(exist_ok=True)
    summary={}
    for locale,name in [('ru_RU','users.csv'),('ro_RO','users-ro.csv')]:
        a=generate(locale);b=generate(locale);assert a==b
        with open('data/'+name,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(a[0]));w.writeheader();w.writerows(a)
        summary[locale]={'rows':len(a),'same_seed_equal':a==b,'sha256':hashlib.sha256(Path('data/'+name).read_bytes()).hexdigest()}
    Path('data/generation.json').write_text(json.dumps(summary,indent=2))
