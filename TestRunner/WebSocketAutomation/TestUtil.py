from bootstrap import *
import json
import re

#deprecated
def extractMessageText(messageObj):
	message = messageObj["cInfo"]["body"]
	if len(message) > 0:
		return message, messageObj["component"]
	else:
		if messageObj["component"] :
			component = messageObj["component"]
			if component["type"] == "text":
				message = component["payload"]["text"]
			elif component["type"] == "template" and component["payload"] and component["payload"]["payload"]:
				message = component["payload"]["payload"]["text"]
	return message, messageObj["component"]

def validateContains(actual, expected):
	aWords = re.split("\W", actual)
	eWords = re.split("\W", expected)
	actualWords = ""
	expectedWords = ""
	for word in aWords:
		if word.strip() != '':
			actualWords = actualWords+" "+word

	for word in eWords:
		if word.strip() != '':
			expectedWords = expectedWords+" "+word

	debug.info("Actual Words:"+actualWords)
	debug.info("Expected Words:"+expectedWords)
	return expectedWords in actualWords

def componentToText(messageObj):
	message = ""
	if messageObj["component"] :
		component = messageObj["component"]
		if component["type"] == "text":
			message = component["payload"]["text"]
		elif component["type"] == "template":
			payload = component.get("payload", None)
			if not payload:
				return message, component
			payload = payload.get("payload", None)
			if not payload:
				return message, component
			templateType = payload.get("template_type",None)
			if templateType == "quick_replies":
				message = payload.get("text", "")
				replies = payload.get("quick_replies", [])
				for reply in replies:
					message += " "+reply.get("title", "")
			elif templateType == "button":
				message = payload.get("text", "")
				buttons = payload.get("buttons", [])
				for button in buttons:
					message += " "+button.get("title", "")
			elif templateType == "list":
				elements = payload.get("elements",[])
				if elements:
					buttons = elements.get("buttons",[])
					for button in buttons:
						message += " "+button.get("title","")
			elif templateType == "error":
				message += " " +payload.get("text","")
			elif templateType == "carousel":
				elements = payload.get("elements",None)
				if elements:
					buttons = elements.get("buttons",[])
					for button in buttons:
						message +=" "+button.get("title","")
			elif templateType == "piechart":
				message = payload.get("text","")
				elements = payload.get("elements",[])
				for element in elements:
					message += " "+element.get("title","")
			elif templateType == "table":
				message = payload.get("text","")
				data = payload.get("data","")
				if data:
					headers = data.get("headers",[])
					for header in headers:
						message +=" "+header.get("title","")
			elif templateType == "barchart":
				message = payload.get("text","")
				elements = payload.get("elements",[])
				for element in elements:
					message +=" "+element.get("title","")
			elif templateType == "linechart":
				message = payload.get("text","")
				elements = payload.get("elements","")
				for element in elements:
					message += " "+element.get("title","")
			else:
				message = json.dumps(component)
				return message, component

		return message, component
	return message, {}