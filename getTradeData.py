import urllib2
import csv
import json
import matplotlib.pyplot as plt
#Sample
#http://www.google.com/finance/getprices?q=GPRO&x=NASD&i=60&p=1d&f=d,c,v,o,h,l&ts=1458552600
#q = stock
#x = exchange
#i = interval
#p = period (how much data)
#f = what you want
#	d = datetime or offset
#	c = close price
#	v = volume
#	o = open
#	h = high
#	l = low

baseUrl = "http://www.google.com/finance/getprices?"
target = open("sampleJson.txt", 'w')

def plotData(dataDict):
	times = []
	closePrices = []
	closeDerivatives = []
	lastClose = dataDict[0]["CLOSE"]
	closeDerivatives2 = []
	lastDeriv = 0
	i = 0
	for obj in dataDict:
		times.append(i)
		closePrices.append(obj['CLOSE'])

		closeDerivatives.append(float(obj["CLOSE"]) - float(lastClose))

		closeDerivatives2.append(float(obj["CLOSE"]) - float(lastClose) - lastDeriv)

		lastDeriv = float(obj["CLOSE"]) - float(lastClose)
		lastClose = obj["CLOSE"]
		i += 1

	fig = plt.figure()
	regPricesPlot = fig.add_subplot(311)
	regPricesPlot.plot(times, closePrices, c='b', marker=".")
	derivativePricesPlot = fig.add_subplot(312)
	derivativePricesPlot.plot(times, closeDerivatives, marker=".")
	derivative2Plot = fig.add_subplot(313)
	derivative2Plot.plot(times, closeDerivatives2, marker=".")
	plt.show()
	'''
	trace0 = go.Scatter(
    x = times,
    y = closePrices,
    name = 'Prices',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
	)
	
	data = [trace0]

	layout = dict(title = 'Close Prices',
		xaxis = dict(title = 'Time (unix timestamp)'),
		yaxis = dict(title = 'Close Prices'),
		)

	fig = dict(data=data, layout=layout)
	py.iplot(fig, filename='styled-line')
	'''


#Will only return the last 10 days of minutely data, but will return
#unlimited amount of 
def requestData(symbol = "AAPL", exchange = "NASD", interval = "60", period = "1d",
	dataWanted = "d,c,o,v,h,l", timeStamp = ""):
	
	url = baseUrl + "q=" + symbol + "&x=" + exchange + "&i=" + interval + "&p=" + period
	url = url + "&f=" + dataWanted

	if timeStamp != "":
		url = url + "&ts=" + timeStamp

	content = urllib2.urlopen(url).read()
	fieldNames = content.splitlines()[4]
	fieldNames = fieldNames[8:]
	fieldNames = fieldNames.split(",")
	reader = csv.DictReader( content.splitlines()[7:], fieldNames)

	out = json.dumps( [ row for row in reader ] )
	dataDict = json.loads(out)
	#print dataDict[0]['DATE'][0]
	
	lastTimeStamp = dataDict[0]['DATE']
	numSinceLastTimeStamp = 1
	for obj in dataDict:
		if obj['DATE'][0] == 'a':
			obj['DATE'] = obj['DATE'][1:]
			lastTimeStamp = int(obj['DATE'])
			numSinceLastTimeStamp = 1
			continue

		obj['DATE'] = str(lastTimeStamp + numSinceLastTimeStamp)
		numSinceLastTimeStamp += 1
	
	target.write(json.dumps(dataDict))
	plotData(dataDict)


requestData()