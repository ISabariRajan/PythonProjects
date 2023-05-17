import json
from time import sleep, time
import requests

def login():
  url = "https://192.168.175.138:5450/webui/login"

  payload='username=uidbadmin&password=Admin%40123&_csrf=dec2bce3-7873-45b4-b0c7-733950ff1b87'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=node017b5ct1rz87jj1snjy8cxln0ac1.node0'
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  # print("logout" in response.text)
  return response

def test():
  url = "https://192.168.175.138:5450/webui/systemConfig/ldap/testConnection?1647340842387="

  SecureLDAP_Test_Path = "C:\\Users\\SSaravananIndra\\Desktop\\Guru\\CustomCodes\\bots\\vertica\\Tests\\LDAPS\\SecureLDAPS_Test.json"
  all_tests = []
  with open(SecureLDAP_Test_Path, "r") as f:
    lines = f.readlines()
    lines = "".join(lines)
    all_tests = json.loads(lines)

  for curr_test in all_tests:
    payload = {
      'data': json.dumps(curr_test)
    }
    # print(json.dumps(all_tests))
    files=[
      ('Wrong_certificate.crt',('Wrong_certificate.crt',open('C:/Users/SSaravananIndra/.ssh/Libo/libo_work/openssl/Wrong_certificate.crt','rb'),'application/octet-stream'))
    ]
    headers = {
      'Cookie': 'JSESSIONID=node017b5ct1rz87jj1snjy8cxln0ac1.node0'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    print(response.text)
    sleep(5)

# payload={'data': '{"ldap.url":"ldap://10.20.41.16:389","ldap.base":"ou=users,dc=example,dc=com","ldap.userDn":"cn=Sabari,ou=users,dc=example,dc=com","ldap.password":"testMC","ldap.bindUser":true,"ldap.secure":true, "ldap.secure.startTLS":true, "ldap.secure.LDAPS":false,"ldap.secure.startTLSOnly":false}'}

# test()
# res = login()
# print(res.status_code)
# print(res.text)

def search():
    url = "https://www.amazon.in/s?k=ceilingfan"
    # url = "https://www.amazon.in/s?k=ceiling+fan&crid=2KOKW22K7HYG9&sprefix=ceiling+fan%2Caps%2C248&ref=nb_sb_noss_1"

    # payload='username=uidbadmin&password=Admin%40123&_csrf=dec2bce3-7873-45b4-b0c7-733950ff1b87'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=node017b5ct1rz87jj1snjy8cxln0ac1.node0'
    }

    response = requests.request("GET", url)

    # print("logout" in response.text)
    return response

res = search()
print(res.text)