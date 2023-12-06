import requests
 
# api-endpoint
URL = "http://127.0.0.1:5000/gas_sense?aq="

for i in range(100):
	x = (i*224807958909389)%621021834215113
	requests.get(URL + str(x%5000))
	print(x%9999)
	
