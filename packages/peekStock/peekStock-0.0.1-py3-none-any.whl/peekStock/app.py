from flask import Flask, render_template, request, redirect, url_for
from crawlerHelper import get_stock, map_together, get_url, get_error, get_value_from_request
crawler_url = 'https://tw.stock.yahoo.com/quote/'

app = Flask(__name__)

app.config['DEBUG'] = True
stock_lst = []

@app.route("/stock/setting", methods=['POST', 'GET'])
def put_stock():
    if request.method == 'POST':
        stock_codes = get_value_from_request(request.form)
        stock_urls = map_together(get_url, stock_codes)
        stock_results = map_together(get_stock, stock_urls)
        error_codes = list(
            filter(None, map_together(get_error, stock_results)))
       
        if error_codes:
            return render_template('setStock.html', error=error_codes)
        return redirect(url_for('stock'))
    else:
        return render_template('setStock.html')

@app.route("/stock/result", methods=['POST'])
def get_stock_result():
    codes_storage = list(request.get_json().values()) 
    stock_urls = map_together(get_url, codes_storage)  
    data = map_together(get_stock, stock_urls)
    return data
    

@app.route("/stock")
def stock():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
