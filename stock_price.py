from bs4 import BeautifulSoup
import re
import requests

# return a dictionary
def batch_code_list():
    # crawling daum finance homepage
    BaseUrl = 'http://finance.daum.net/quote/all.daum?type=S&stype='

    # 'P' : Kospi
    # 'Q' : Kosdaq
    markets = {'P', 'Q'}
    code_dic = {}

    for market in markets :
        url = BaseUrl + market
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find_all('td', {'class': 'txt'})

        for item in items:
            txt = item.a.get('href')
            k = re.search('[\d]+', txt)
            if k :
                code = k.group()
                kname = item.text
                # only Kospi, Kosdaq extract
                if len(code) != 6:
                    continue

                # make { code : kname } dictionary
                code_dic[code] = kname

    return code_dic

def get_current_price(code):
    # crawling daum finance homepage
    BaseUrl = 'http://finance.daum.net/item/main.daum?code=' + code
    r = requests.get(BaseUrl)
    soup =BeautifulSoup(r.text, 'lxml')

    items = soup.find_all('dd', 'txt_price')
    # items[0] : yesterday price, 전일종가
    # items[1] : high price, 고가
    # items[2] : upper limit price, 상한가
    # items[3] : start price, 시가
    # items[4] : low price, 저가
    # itmes[5] : lower limit price, 하한가

    # current price
    prpr = soup.find('em', 'curPrice')

    # rate (curPrice - yesterday price / yesterday price)
    rateup = soup.find('span', 'rate')

    # I just want to get JSON fmt and remove '+', '-'
    return {'code': code, 'price': prpr.text, 'rate': rateup.text,
            'hist': items[0].text.replace("+", "").replace("-", ""),
            'start': items[3].text.replace("+", "").replace("-", ""),
            'high': items[1].text.replace("+", "").replace("-", ""),
            'low': items[4].text.replace("+", "").replace("-", "")}


if __name__ == '__main__' :
    print(batch_code_list())
    print(get_current_price('000660'))
