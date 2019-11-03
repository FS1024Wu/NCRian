import http.client

conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")

headers = {
    'content-type': "application/json",
    'enterprise-unit-id': "String"
    }

conn.request("GET", "/nr1dc/offerline/hospitality/promotions?EffectiveDate=String&StartDate=String&EndDate=String&Name=String&OriginPromotionId=String&PosPromotionId=String&IsActive=SOME_BOOLEAN_VALUE&PageNumber=35&PageSize=15", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
