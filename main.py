import requests
from bs4 import BeautifulSoup
import json

URL_ROOT = 'https://www.eldorado.ru'
URL = "https://www.eldorado.ru/cat/detail/smartfon-apple-iphone-11-128gb-black-mhdh3ru-a/?show=response#customTabAnchor"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Accept": "*/*"
}


def get_html(url, params=None):
    r = requests.session().get(url, headers=HEADERS, params=params)
    return r


def get_button_next(html):
    soup = BeautifulSoup(html, "html.parser")
    button_next = soup.find('a', class_="button buttonNext").get('href')
    return button_next


response = []


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all(class_="usersReviewsListItemInnerContainer")

    for item in items[1:]:
        name = item.find("div", class_="userInfo")
        city = item.find("span", class_="userFrom")
        text = item.find("div", class_="middleBlockItem")
        if text:
            text.p.extract()
        rating = item.find("div", class_="itemRate")
        rating2 = rating.find_all("div", class_="starFull") if rating else None
        data = item.find("div", class_="userReviewDate")

        response.append({
            "name": name.span.get_text(strip=True) if name else None,
            "city": city.get_text(strip=True) if city else None,
            "text": text.get_text(strip=True) if text else None,
            "rating": len(rating2) if rating2 else None,
            "date": data.get_text(strip=True) if data else None,
        })

    return response


finally_information = []


def save_file():
    finally_information.append(response)
    with open("reviews.json", "w", encoding='utf-8') as write_file:
        json.dump(finally_information, write_file, ensure_ascii=False, indent=2)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.content)
        next_url = get_button_next(html.text)
        try:
            while next_url:
                print(''.join([URL_ROOT, next_url]))
                html = get_html(''.join([URL_ROOT, next_url])).content
                get_content(html)
                next_url = get_button_next(html)
        except AttributeError:
            return False
    else:
        print("Error")


parse()
save_file()
