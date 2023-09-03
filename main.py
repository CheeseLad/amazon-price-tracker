#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime

db = orm.Database()
db.bind(provider = "sqlite", filename = "amazon_products.db", create_db = True)

class Product(db.Entity):
  name = orm.Required(str)
  price = orm.Required(float)
  price_date = orm.Required(datetime)


db.generate_mapping(create_tables = True)

def getPrice(session):
  url = str(input("Enter your Amazon URL here: "))
  response = session.get(url)
  soup = BeautifulSoup(response.text, "html.parser")
  data = (
    #soup.select_one("div.celwidget span.a-size-large product-title-word-break"),
    "amazon",
    float(soup.select_one("div.a-box-group span.a-offscreen").text.replace("£", "").replace(",", "")),
  )
  return data


def main():
  session = requests.Session()
  session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
  })

  amazon = getPrice(session)
  #print(amazon)

  with orm.db_session:
    Product(name = amazon[0], price = amazon[1], price_date = datetime.now())
    print("Done!\nCheck amazon_products.db for your result!")

if __name__ == "__main__":
  main()

  #test = soup.select_one("span.a-price aok-align-center reinventPricePriceToPayMargin priceToPay span.a-price-whole").text
  #print(test)

#sessionnew = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"

#getPrice(sessionnew)