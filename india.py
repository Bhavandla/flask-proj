from nsetools import Nse

nse = Nse()

def nse_quote(code):
    q = nse.get_quote(code)
    return q