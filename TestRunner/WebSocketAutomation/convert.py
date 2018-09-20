import json

def convertToTestSuite(jsonFileName):
	keys = ["botId", "type", "userId", "timeStamp", "channel", "message"]
	testCases = []
	with open("converted_"+jsonFileName, 'w') as testSuiteFile:
		with open("recorded/"+jsonFileName, "r") as file:
			testCase = None
			for line in file:
				messageObj = json.loads(line)
				resourceid = messageObj.get("resourceid", None)
				msgType = messageObj.get("type", None)
				if resourceid == '/bot.message' and not msgType == 'ping':
					testCase = {
						"messages":[]
					}
					testCases.append(testCase)
					print(messageObj["clientMessageId"])
					inputText = messageObj["message"]["body"]
					testMessage = {}
					testCase["messages"].append(testMessage)
					testMessage["input"] = inputText
					testMessage["outputs"] = []
					continue
				if messageObj["type"] == "bot_response":
					message = messageObj["message"][0]
					output = {}
					if message["type"] == "text":
						text = message["component"]["payload"]["text"]
						output["contains"] = text
					testCases[-1]["messages"][-1]["outputs"].append(output)
					continue
	str = json.dumps(testCases)
	print(str)





convertToTestSuite("record1.json")