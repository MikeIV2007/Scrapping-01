import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
import json

"""
Потрібно реалізувати клас який буде взаємодіяти зі стороннім API: API (https://restcountries.com) Клас повинен отримувати дані від API то повертати в консоль в табличній формі, а саме такі дані: назва країни, назва столиці та посилання на зображення прапору в форматі png.
"""

class CountryInfo:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"

    def get_country_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error fetching data from API")

    def display_country_info(self):
        country_data = self.get_country_data()
        table_data = []

        for country in country_data:
            name = country.get('name', {}).get('common', 'N/A')
            capital = country.get('capital', ['N/A'])[0]
            flag_url = country.get('flags', {}).get('png', 'N/A')
            table_data.append([name, capital, flag_url])

        print(tabulate(table_data, headers=["Country Name", "Capital", "Flag URL"], tablefmt="grid"))

"""
Потрібно створити клас який буде збирати дані за посиланням на Ebay сторінку товару, формат даних в якому повинні повертатись дані json в тестовому завданні можна просто виводити в консоль, або зберігати в файл. Обов’язкові дані це назва, посилання на фото, саме посилання на товар, ціна, продавець, ціна доставки. Авжеж чим більше даних, тим краще, але в контексті тестового це не важливо.
"""

class EbayScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"Error fetching data from Ebay: {err}")

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('h1', {'class': 'x-item-title__mainTitle'})
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'

        image_tag = soup.find('img', {'data-idx': '0'})
        image_url = image_tag['src'] if image_tag else 'N/A'

        price_tag = soup.find('div', {'class': 'x-price-primary'})
        if price_tag:
            price_span = price_tag.find('span', {'class': 'ux-textspans'})
            price = price_span.get_text(strip=True) if price_span else 'N/A'
        else:
            price = 'N/A'

        seller_div = soup.find('div', {'class': 'vim x-sellercard-atf'})
        if seller_div:
            seller_tag = seller_div.find('span', {'class': 'ux-textspans--BOLD'}) or seller_div.find('span', {'class': 'ux-textspans'})
            seller = seller_tag.get_text(strip=True) if seller_tag else 'N/A'
        else:
            seller = 'N/A'

        shipping_div = soup.find('div', {'data-testid': 'ux-labels-values', 'class': 'ux-labels-values--shipping'})
        if shipping_div:
            shipping_span = shipping_div.find('span', {'class': 'ux-textspans--BOLD'})
            shipping_price = shipping_span.get_text(strip=True) if shipping_span else 'N/A'
        else:
            shipping_price = 'N/A'

        data = {
            'title': title,
            'image_url': image_url,
            'product_url': self.url,
            'price': price,
            'seller': seller,
            'shipping_price': shipping_price
        }
        return data

    def save_data(self, data, filename='ebay_product_data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

    def run(self):
        try:
            html = self.fetch_page()
            data = self.parse_page(html)
            self.save_data(data)
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(e)



if __name__ == "__main__":
    # python scraping_01.py

    country_info = CountryInfo()
    country_info.display_country_info()


    ebay_url = "https://www.ebay.com/itm/276278279068?itmmeta=01J2BR8Z1NCYGJQ69R0335YAMC&hash=item405377fb9c:g:ijgAAOSwyWVmXyMz&amdata=enc%3AAQAJAAAA0M4aecH3qWPVfpgbYu5ZRaddLI1zVXX5VGCdZU3zfwg0P52pvTD2lZY9swdDLudEXQ3wmKEn4WqtyAHk9kZy%2Bm5DNhgxtKjYOQatQaPKPoELlrJE%2B3EFw2Zn9TqIyQK3notX7Io7sbo%2BuCnENKr1eM4aecH3qWPVfpgbYu5ZRaddLI1zVXX5VGCdZU3zfwg0P52pvTD2lZY9swdDLudEXQ3wmKEn4WqtyAHk9kZy%2Bm5DNhgxtKjYOQatQaPKPoELlrJE%2B3EFw2Zn9TqIyQK3notX7Io7sbo%2BuCnENKr1eZHSvVQLHa%2FbkPN32SDbC3GkLEnqSiqo6c1zcMXvjnlKPhOed92BQNkmsZmobCFi%2Fw6fM7LGcuGGB5il6XYMET5Fe5jOoIt%2F9uYcF0outCbGDVqGzXbwmKa7SvzZPcD1rKo%3D%7Ctkp%3AB"

    #ebay_url = "https://www.ebay.com/p/8041719718?iid=296392586904"

    #ebay_url = "https://www.ebay.com/itm/185272596536?itmmeta=01J2BZRSA64HN07Z8V95G3CAQK&hash=item2b231b7838:g:D6wAAOSw-4Nkq~QO"
    
    #ebay_url = "https://www.ebay.com/itm/176460405053?itmmeta=01J2BZRSA6D9D3STVQMR1T07Y3&hash=item2915dc193d:g:CygAAOSwrIpmV1Hc"

    ebay_scraper = EbayScraper(ebay_url)
    ebay_scraper.run()

