import requests


def currency_data(have, want, amoun):
	url = "https://currency-converter-by-api-ninjas.p.rapidapi.com/v1/convertcurrency"

	querystring = {"have":have,"want":want,"amount":amoun}

	headers = {
	"X-RapidAPI-Key": "d20426d2femsh57870040d686a7fp113d72jsn0c59374bb543",
	"X-RapidAPI-Host": "currency-converter-by-api-ninjas.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	respond=response.json()
	data=respond['new_amount']
	return data




