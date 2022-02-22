from pkgutil import get_data
import requests
from bs4 import BeautifulSoup
from time import sleep
import csv      


MAIN_URL = "https://www.list.am/category/60?gl=2"
BASE_URL = "https://www.list.am"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class ListParser:
    def __init__(self, url) -> None:
        self.url = url
        self.soup = None

    def __get_main_page(self, page_number: int):
        page = requests.get(self.url.format(page_number), headers=HEADERS)
        self.soup = BeautifulSoup(page.content,'lxml')
        my_divs = self.soup.find_all("div",attrs = {"class": "dl"})
        return my_divs

    

    def parse_data(self, url):
        item_page = requests.get(url, headers= HEADERS)
        item_soup = BeautifulSoup(item_page.content, 'lxml')
        item_div = item_soup.find("div", attrs={"id":"attr"})
        if item_div is None:
            return None
        data_dict = {}
        infos = item_div.find_all("div",attrs={"class":"c"})
        price_info = item_soup.find("span",attrs={"class":"price"})
        loc_info = item_soup.find("div",attrs={"class":"loc"})
        if price_info is None:
            price_info = "Not Defined"
            data_dict["Price"] = price_info
        else:
            data_dict["Price"] = price_info.text
        if loc_info is None:
            loc_info = "Not Defined"
            data_dict["Location"] = loc_info
        else:
            data_dict["Location"] = loc_info.text
        
        for info in infos:
            data_dict[(info.div.string)] = info.find("div",attrs= {"class":"i"}).string
            
        return data_dict
            
    def get_data(self):
        for i in range(1,251):
            print(self.url.format(i))
            my_divs = self.__get_main_page(i)
            # if i != 1 and self.__get_current_page_number() == 1:
            if i > 5:
                return []
            data_list = []
            for my_div in my_divs:
                for link in my_div.find_all("a"):
                    # sleep(1)
                    info_url = f"{BASE_URL}{link['href']}"
                    if "item" in info_url:
                        data = self.parse_data(info_url)
                        if data is not None:
                            data_list.append(data)
        return data_list

    def filter_by_date(self, data):
        return True

    def __get_current_page_number(self):
        next_page = self.soup.find("div", attrs = {"class": "dlf"})
        next_page = next_page.find('span', attrs = {"class": "pp"})
        return int(next_page.span.string)
    
    def save_to_csv(self, file_name):
        dict_list = self.get_data()
        csv_columns = list(dict_list[0].keys())

        try:
            with open(file_name, 'w', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator='\n')
                writer.writeheader()
                for data in dict_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


    





if __name__ == '__main__':
    main_url = "https://www.list.am/category/60/{}?gl=2"
    print(main_url.format(2))
    parser = ListParser(main_url)
    parser.save_to_csv("List_am.csv")
    # parser.parse_data("https://www.list.am/item/17114665")


