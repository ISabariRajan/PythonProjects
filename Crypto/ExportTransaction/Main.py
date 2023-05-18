import requests

ETHER_API_KEY = "PK8U12HPFN9XVX9IZ3CZCUUXHQ1A3SIFQ3"
# contract_address = input("Enter Contract Address: ")

contract_address = "0x9cbf044bc535db4c93a9f11205a69631d9dcef26"
request_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHER_API_KEY}"
print(request_url)
response = requests.get(request_url)
results = response.json()["result"]
keys = results[0].keys()
print(len(results), keys)

with open("output.csv", "w") as f:
    f.write(",".join(keys) + "\n")
    for result in results:
        line = ""
        for key in keys:
            line += result[key] + ", "
        f.write(line + "\n")

# print(response.json().keys())
# https://api.etherscan.io/api?module=account&action=txlist&contractaddress=0x9cbf044bc535db4c93a9f11205a69631d9dcef26&sort=asc&api_key=