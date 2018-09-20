from TestSuite import *
import json
from html.parser import HTMLParser

def writeResults(name, countpass, countfail):
		print("SuiteName:",name)
		print("FAILED", countfail)
		print("PASSED", countpass)
		print("TOTAL CASES EXECUTED",(countfail+countpass))
		f = open(resultsHtml,'a')
		message = """<html>
						<head>
							<style>
								table, th, td {
									border: 1px solid black;
								}
							</style>
						</head>
						<body>
							<br />
							<table width="200">
							<tr>
								<th style="width:70%"><font size="2">""" + str(name) + """</font></th>
								<th style="width:30%"><font size="2">Count</font></th>
							</tr>
							<tr>
								<td>Pass</td>
								<td style="color:green; font-weight:bold">""" + str(countpass) + """</td>
							</tr>
							<tr>
								<td>Fail</td>
								<td style="color:red; font-weight:bold">""" + str(countfail) + """</td>
							</tr>
							<tr>
								<td>Total</td>
								<td style="color:orange; font-weight:bold">""" + str(countfail + countpass)+"""</td>
							</tr>
							</table>

						</body>
					</html>"""
		# message  = message.format(countpass=str(self.countpass),countfail=str(self.countfail),counttotal=str(self.total))        
		# return message
		f.write(message)
		f.close()


f = open(resultsHtml,'w')
f.close()
with open(testSuiteFile) as data_file:
	data = json.load(data_file)
	for testName in data["testCases"]:
		testSuite = TestSuite(testName)
		countpass, countfail = testSuite.begin()
		testName = testName.split("/")[-1]
		writeResults(testName, countpass, countfail)