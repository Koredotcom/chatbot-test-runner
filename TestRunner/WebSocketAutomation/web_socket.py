from bootstrap import *
from websocket import create_connection
import json
import time
import threading
from datetime import datetime
import ssl

class WebSocketClient( object ):
	

	def __init__(self, url, botId, botName, welcomeMessageCount=0):
		self._url = url
		self.ws = None
		self.run = True
		self._botName = botName
		self._botId = botId
		self.welcomeMessageCount = welcomeMessageCount
		self.pinger = None
		if IS_BUILDER :
			self.client = "botbuilder"
		else:
			self.client = "sdk"
		
	def connect (self):
		sslopt={"cert_reqs": ssl.CERT_REQUIRED}
		if not VERIFY_SSL_CERT:
			sslopt={"cert_reqs": ssl.CERT_NONE}
			
		self.ws = create_connection(self._url, sslopt=sslopt)
		i=0
		while i < self.welcomeMessageCount :
			self.receiveOne()
			i+=1
		debug.info ("Connection opened")
		self.pinger = threading.Thread(target=self.ping)
		self.pinger.start()

	
	def sendMessage(self, text, expectedResCount):
		messageId = 0
		messageId = datetime.now()
		id = time.time()*1000
		message = '{"clientMessageId":'+str(id)+',"message":{"body":"'+text+'"},"resourceid":"/bot.message","botInfo":{"chatBot":"'+self._botName+'","taskBotId":"'+self._botId+'"},"client":"'+self.client+'","meta":{"timezone":"Asia/Kolkata","locale":"en-US"},"id":'+str(id)+'}'
		debug.info (str(expectedResCount)+" User Input::"+text)
		self.ws.send(message)
		i = 0
		responses = []
		while i < expectedResCount :
			diff = datetime.now() - messageId
			#print (str(diff.seconds), messageId)
			
			if diff.seconds > 30:
				debug.info("%s %s %s",responses, diff.seconds, messageId)
				return responses
			
			result =  self.ws.recv()
			#print(result)
			messageJson = json.loads(result)
			if messageJson["type"] == 'bot_response' and messageJson.get("message"):
				i = i+1
				if len(messageJson["message"]) > 0:
					responses.append(messageJson["message"][0])
				
		
		debug.info(responses)			
		return responses
	
	
	def ping(self):
		i = 1
		while self.run :
			time.sleep(2)
			message = '{"type":"ping","resourceid":"/bot.message","botInfo":{"chatBot":"'+self._botName+'","taskBotId":"'+self._botId+'"},"client":"'+self.client+'","meta":{"timezone":"Asia/Kolkata","locale":"en-US"},"id":'+str(i)+'}'
			i = i+1
#			print ("Pinging")
			try:
				self.ws.send(message)
			except Exception as e:
				pass
				break
			
	def receiveOne(self):
		result =  self.ws.recv()
  #	  print(result)
		messageJson = json.loads(result)
		if messageJson["type"] == 'bot_response' and messageJson.get("message"):
			if len(messageJson["message"]) > 0:
				return messageJson["message"][0]["cInfo"]["body"]
			return ""
		return self.receiveOne()
	
	def close(self):
		self.run = False
		time.sleep(2)
		self.ws.close()
			
