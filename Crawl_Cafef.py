import requests
from bs4 import BeautifulSoup
import pandas as pd

class StockScraper:
    def __init__(self):
        self.base_url = 'https://cafef.vn'

    def get_top_stock(self):
        try:
            res = requests.get(f'{self.base_url}/get-top-stock.chn')
            data = res.json()['stocks']
        except:
            return "Không thể tìm nạp dữ liệu"
        return data

    def get_info_stock(self, stock_name):
        try:
            res = requests.get(f'{self.base_url}/info.ashx?type=cp&symbol={stock_name}')
            data = res.json()
        except:
            return "Không thể tìm nạp dữ liệu hoặc mã cổ phiếu cần tìm bị sai"
        return data

    def get_list_post(self, page_num):
        try:
            res = requests.get(f'{self.base_url}/timelinelist/18831/{page_num}.chn')
            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find_all(class_='tlitem box-category-item')
        except Exception as e:
            return f"gặp lỗi: {e}"
        return data

    def get_info_post(self, data):
        times = []
        desc = []
        links = []
        titles = []
        for i in range(len(data)):
            times.append(data[i].find(class_='time time-ago').text)
            desc.append(data[i].find(class_='sapo box-category-sapo').text)
            links.append(self.base_url + data[i].find('a', href=True)['href'])
            titles.append(data[i].find('a', href=True).text)
        return times, desc, links, titles

    def get_content_post(self, link_post):
        content = ''
        try:
            res = requests.get(link_post)
            soup = BeautifulSoup(res.content, 'html.parser')
            c = soup.find(class_='detail-content afcbc-body')
            p = c.find_all('p')
            for i in range(len(p)):
                content = content + p[i].text + '\n'
        except Exception as e:
            return f"gặp lỗi: {e}"
        return content

    def scrape_and_save_to_csv(self, num_pages, output_file):
        df = pd.DataFrame()
        for i in range(1, num_pages+1):
            content = []
            times, desc, links, titles = self.get_info_post(self.get_list_post(i))
            for j in range(len(links)):
                content.append(self.get_content_post(links[j]))
            temp_df = pd.DataFrame({'Title': titles, 'Desc': desc, 'Content': content, 'Link': links, 'Time': times})
            df = pd.concat([df, temp_df])
        df.to_csv(output_file, index=False)
        print("Dữ liệu đã được lưu vào file CSV.")

# Sử dụng phương thức scrape_and_save_to_csv để thu thập dữ liệu và lưu vào file CSV
scraper = StockScraper()
scraper.scrape_and_save_to_csv(15, 'stock_data.csv')
