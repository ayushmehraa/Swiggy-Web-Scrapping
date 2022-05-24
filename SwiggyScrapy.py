import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml
# Using following code we can fake the agent to bypass server to authorize it.

# using header to counter 403 error(The HTTP 403 Forbidden response status code indicates that the server understands the request but refuses to authorize it)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

place = input("Enter location:\n").lower()
# swiggy server dosen't give 403 response but zomato server does
url = f'https://www.swiggy.com/{place}/'
req = requests.get(url, headers=headers)

content = req.text
# creating a local html file
# with open('swiggy.html','w+',encoding="utf-8")as file:
#     file.write(content)

soup = BeautifulSoup(content, "lxml")
# restBox=soup.find_all("div",class_="_3XX_A")
restBox = soup.find_all("div", class_="_3FR5S")
# rests=restBox[0].find_all("a",class_="_1j_Yo")
RestList = []
for rest in restBox:
    dataframe = {}
    try:
        dataframe['Rests Name'] = rest.find("div", class_="nA6kb").text
        dataframe['Cuisine'] = rest.find("div", class_="_1gURR").text
        dataframe['Price'] = rest.find("div", class_="nVWSi").text
        dataframe['Offer'] = rest.find("span", class_="sNAfh").text
        timeAndRating = rest.find("div", class_="_3Mn31")
        dataframe['Time'] = timeAndRating.text[4:10]
        dataframe['Rating'] = timeAndRating.text[0:3]
    except:
        pass
        # try:
        #     print("Name: "+restsName+"\nCusine: "+cuisine+"\nPrice: "+price+"\nOffer: "+offer.text+"\nTime: "+time+"\nrating: "+rating+"\n")
        # except :
        #     pass
    RestList.append(dataframe)

df = pd.DataFrame(RestList)
df.to_csv(f'SwiggyScrapy{place}.csv', index=False)

print('Done!!')