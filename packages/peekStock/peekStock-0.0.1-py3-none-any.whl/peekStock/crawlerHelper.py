from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor

def get_stock(url):
    web = requests.get(url)
    soup = BeautifulSoup(web.text, "html.parser")
    error = None
    if web.status_code == 404:
        error = url + "/Error"
        return error
    company = soup.select('h1')[1].get_text()
    quote = soup.find('span', {'class': 'Fz(32px)'})
    difference = soup.find('span', {'class': 'Fz(20px)'}).get_text()

    up_or_down = ''
    if "C($c-trend-up)" in quote.attrs["class"]:
        up_or_down = '+'
    elif "C($c-trend-down)" in quote.attrs["class"]:
        up_or_down = '-'
    else : 
        up_or_down = '-'

    return (f'{ company } : { quote.get_text() } ( { up_or_down }{ difference } )')

def get_error(url):
    if "Error" in url:
        return url.split('/')[4]
    
def map_together(func, lst):
    data = []
    executor = ThreadPoolExecutor()
    with ThreadPoolExecutor() as executor:
        data = list(executor.map(func, lst))
    return data

def get_url(codes):
    url = 'https://tw.stock.yahoo.com/quote/'
    return f'{url}{codes}'

def get_value_from_request(request):
    lst = []
    for idx in request:
        stock_code = request.getlist(idx)[0]
        if stock_code != "":
            lst.append(f'{stock_code}')
    return lst
