import requests

headers = {
	'accept-encoding': "gzip, deflate, br",
	'accept-language': "en-US,en;q=0.8,hi;q=0.6",
	'content-type': "application/json",
	'accept': "application/json",
	'connection':'keep-alive',
	'dnt': "1"
}

ses=requests.session()
def loginToKore(platform, koreUserId,KorePassword):
	url = platform+"/oauth/token"
	payload = "{\"client_id\":\"1\",\"client_secret\":\"1\",\"scope\":\"1\",\"grant_type\":\"password\",\"username\":\""+koreUserId+"\",\"password\":\""+KorePassword+"\"}"
	print(url, payload, headers)
	response = requests.post(url, data=payload, headers=headers)
	print(response.status_code, url, payload)
	return response.json()['authorization']['accessToken']

def sts(platform, authTokenLogin):
	url = platform+"/users/sts"
	headers ['authorization']= "bearer "+authTokenLogin
	response = requests.post( url, headers=headers)
	print("response.json()", response.json())
	return response.json()["jwt"]

def jwt(platform, botId, botName, bearer):
	payloadrtm = "{\"assertion\":\""+bearer+"\",\"botInfo\":{\"chatBot\":\""+botName+"\",\"taskBotId\":\""+botId+"\"},\"token\":{}}"
	url = platform+"/oAuth/token/jwtgrant"
	response = requests.post( url, data=payloadrtm, headers=headers)
	return response.json()["authorization"]["accessToken"]

def getRTMAuthToken(platform, botId, botName, username, password):
	print(platform, username, password)
	token = loginToKore(platform, username, password)
	print("token1", token)
	jwToken = sts(platform, token)
	print("jwt", jwt)
	return jwt(platform, botId, botName, jwToken)
