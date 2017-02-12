from googlefinance import getQuotes
from yahoo_finance import Share
import finsymbols




def get_quote(ticker):

	yahoo = Share(ticker)
	quote = getQuotes(ticker)[0]['LastTradePrice']
	index = getQuotes(ticker)[0]['Index']
	code = getQuotes(ticker)[0]['StockSymbol']
	open_price = yahoo.get_open()

	return yahoo, quote, index, open_price, code


