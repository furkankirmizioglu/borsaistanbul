from datetime import datetime, timedelta

from flask import Flask, request
from flask_restful import Api
from numpy import array
from pandas import DataFrame
from yahoo_fin.stock_info import get_data

app = Flask(__name__)
api = Api(app)


@app.route('/price', methods=['GET'])
def get_current_price():
    now = datetime.now() + timedelta(days=1)
    one_year_ago = now - timedelta(days=2)
    stock_data = get_data(ticker="{}.IS".format(request.args.get('ticker')),
                          start_date=one_year_ago.strftime("%Y/%m/%d"),
                          end_date=now.strftime("%Y/%m/%d"),
                          index_as_date=True,
                          interval='1d')

    close_data = DataFrame.to_numpy(stock_data)
    price_list = array([float(x[3]) for x in close_data])
    price = round(price_list[-1], 2)

    del stock_data
    del now
    del one_year_ago
    del close_data

    response_dict = {
        "price": price
    }

    return response_dict


if __name__ == "__main__":
    app.run(host="localhost", port=8090)
