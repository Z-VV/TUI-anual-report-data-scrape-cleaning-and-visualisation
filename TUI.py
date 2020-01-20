import bs4 as bs
from bs4 import BeautifulSoup as soup
import sys
import time
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

def links():
    page_list = []
    page = Page('https://www.tuigroup.com/en-en/investors/key-financial-information/2019/key-figures-q1-2019')
    page1 = Page('https://www.tuigroup.com/en-en/investors/key-financial-information/2019/key-figures-q2-2019')
    page2 = Page('https://www.tuigroup.com/en-en/investors/key-financial-information/2019/key-figures-q3-2019')
    page_list.append(page)
    page_list.append(page1)
    page_list.append(page2)
    return page_list

def scrape(page):
    page_soup = soup(page.html, 'html.parser')
    articles = page_soup.find_all('article')
    article = articles[0]
    return article

def collecting_data_from_tables(article):
    header = article.thead.find_all('th')[1:4]
    lines = article.tbody.find_all('tr')
    return header,lines

def cleaning_data(first_4_rows):
    first = first_4_rows[0].text
    second = first_4_rows[1].text
    third = first_4_rows[2].text
    forth = first_4_rows[3].text
    if '\n' in first:
        first = first.split('\n')[1]
        second = second.split('\n')[1]
        third = third.split('\n')[1]
        forth = forth.split('\n')[1]
    forth = [str(r) for r in forth]
    del forth[1]
    forth = [i.replace('–', '-') for i in forth]
    forth = ''.join(forth)
    forth = float(forth)
    second = float(second.replace(',', ''))
    third = float(third.replace(',', ''))
    return first, second, third, forth

def creating_clean_dataframe(header,lines):
    data = pd.DataFrame(columns=['business', header[0].text,  header[1].text, header[2].text])
    for x in range(len(lines)):
        first_4_rows = lines[x].find_all('td')[0:4]
        first,second,third,forth = cleaning_data(first_4_rows)
        dic = {'business':first , header[0].text :second ,header[1].text :third , header[2].text :forth}
        data = data.append(dic, ignore_index=True, sort=False)
    print(data)

    return data

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 7),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def data_visualisation(data):
    global ax
    labels = data.iloc[:,0]
    Q1_2018 = data.iloc[:,1]
    Q1_2019 = data.iloc[:,2]

    x = np.arange(len(labels))
    width = 0.38

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, Q1_2018, width, label=data.columns[1])
    rects2 = ax.bar(x + width / 2, Q1_2019, width, label=data.columns[2])

    ax.set_ylabel('€ million')
    ax.set_title('TURNOVER')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    fig.autofmt_xdate()
    plt.show()


def main():
    page_list = links()
    for x in page_list:
        article = scrape(x)
        header,lines = collecting_data_from_tables(article)
        data = creating_clean_dataframe(header,lines)
        data_visualisation(data)

main()










