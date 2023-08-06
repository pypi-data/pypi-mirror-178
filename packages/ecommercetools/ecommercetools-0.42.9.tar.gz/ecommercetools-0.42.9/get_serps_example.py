from ecommercetools import seo

df = seo.get_serps("bmw", pages=1, domain="google.de", host_language="de")

print(df)