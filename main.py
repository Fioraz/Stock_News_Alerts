import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
news_dict = {}
increment = "🔺"
decrement = "🔻"
account_sid = "ACCOUNT_SID"
auth_token = "AUTH_ToKEN"
STOCKS_API = "STOCK_API_KEY"
NEWS_API = "NEWS_API_KEY"
MOBILE_NUMBER = "YOUR_MOBILE_NUMBER"

stocks_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKS_API,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apikey": NEWS_API,
}


def stock_price():
    response = requests.get("https://www.alphavantage.co/query", params=stocks_parameters)
    stock_data = response.json()
    dict_values = list(stock_data["Time Series (Daily)"].values())
    # dict_values = [value for (key, value) in data.item()]
    yesterday = float(dict_values[0]["4. close"])
    d_before_y = float(dict_values[1]["4. close"])
    price_difference = yesterday - d_before_y
    return (price_difference / yesterday) * 100


def get_news():
    response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news = response.json()["articles"][:3]
    for x in range(3):
        news_dict[x] = [news["title"], news["url"]]
    return news_dict


client = Client(account_sid, auth_token)
percentage = int(stock_price())
if percentage > 0:
    message_heading = f"{STOCK}: {increment}{percentage}%"
else:
    message_heading = f"{STOCK}: {decrement}{abs(percentage)}%"

client.messages.create(
    body=f"{message_heading}\n"
         f"Headline: {get_news()[0][0]}. \nBrief: {get_news()[0][1]}\n"
         f"Headline: {get_news()[1][0]}. \nBrief: {get_news()[1][1]}\n"
         f"Headline: {get_news()[2][0]}. \nBrief: {get_news()[2][1]}",
    from_='+447700000000',
    to=MOBILE_NUMBER
)
