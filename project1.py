import requests
import pandas as pd
from bs4 import BeautifulSoup as bs4

titles = []
prices = []
status = []
picture_urls = []
stars = []

# We can use while if we don't know number of pages. Break while loop if content.status is 404.
for page_number in range(1,51): 
    page_url = "http://books.toscrape.com/catalogue/page-{}.html".format(page_number)
    content = requests.get(page_url)

    soup = bs4(content.text, "html.parser")

    blocks = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for title in blocks:
        titles.append(title.find("h3").find("a")["title"])

    for price in blocks:
        prices.append(price.find("div", class_="product_price").find("p", class_="price_color").text)
        status.append((price.find("div", class_="product_price").find("p", class_="instock availability").
                       text).strip())

    for pic in blocks:
        picture_urls.append("http://books.toscrape.com/"+
              pic.find("div", class_="image_container").find("img")["src"].replace("../",""))

    for star in blocks:
        for k,v in star.find("p", class_="star-rating").attrs.items():
            stars.append(v[1])

df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Status": status,
    "Picture URL": picture_urls,
    "Stars": stars,    
})
df.index+=1

#df.style.set_properties(**{'text-align': 'left'}) # inorder to align column values to left

df
