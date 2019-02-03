from urllib import request
from bs4 import BeautifulSoup as soup 
from selenium import webdriver
import sqlite3

class DBfor():
    def create_database():
        global con
        global c 
        con = sqlite3.connect('scraped.db')
        c = con.cursor()
        try:
            c.execute("""CREATE TABLE scraped(
            name text,
            studio text,
            episodes text
            )""")
        except:
            print("table created ")
   
    def database(name,studio,episodes):
        c.execute("INSERT INTO scraped VALUES(?,?,?)",(name,studio,episodes))
        con.commit()
        c.execute("select name from scraped")


class Scrapedata():
    def __init__(self,link):
        self.link = link
        opened= request.urlopen(link)
        self.soup_obj = soup(opened,"html.parser")

db_start = DBfor.create_database()

web_1= Scrapedata("https://myanimelist.net/anime/season/schedule")
blocks= web_1.soup_obj.select("div.seasonal-anime-list.js-seasonal-anime-list.clearfix")


for block in blocks:
    day = block.find("div",{"class","anime-header"}).get_text()
    content = block.find_all("div",{"class","seasonal-anime js-seasonal-anime"})
    for anime in content:
        try:
            name = anime.find("p",{"class","title-text"}).a.get_text()
            studio = anime.find("span",{"class","producer"}).a.get_text()
            episodes = anime.find("div",{"class":"eps"}).get_text(strip = True)
            
        except AttributeError :
            studio = "no studio"
        DBfor.database(name, studio, episodes)
data = c.fetchall()
            
driver = webdriver.Chrome(r"C:\Users\nik\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("https://anidex.info/")
driver.implicitly_wait(20)
search = driver.find_element_by_id("quick_search_input")
submit = driver.find_element_by_id("quick_search_button")
search.send_keys(data[0])
submit.click()
url_1= driver.current_url
print(url_1)

con.close()

