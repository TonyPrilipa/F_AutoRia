import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url = 'https://auto.ria.com/search/' \
           '?categories.main.id={0}&' \
           'price.currency={1}&' \
           'price.USD.gte={2}&' \
           'price.USD.lte={3}&' \
           'region.id[0]={4}&' \
           'brand.id[0]={5}&' \
           'model.id[0]={6}&' \
           'year[0].gte={7}&' \
           'year[0].lte={8}'


# category_id = '1' # легковые format 0
# price_currency = '1' # USD   format 1
# price_from = '100'   #       format 2
# price_to = '10000'   #       format 3
# region_id = '10'     # Kyiv  format 4
# brand_id = '6'       # Audi  format 5
# model_id = '39'      # 100   format 6
# year_from = '1990'   #       format 7
# year_to = '2020'     #       format 8


def get_html(url):
    r = requests.get(url)
    return r.text


def write_response(text):
    f = open('response.html', 'w', encoding='utf-8')
    f.write(text)
    f.close()


def get_items(text):  # function returns bs4.element.Tag list
    soup = BeautifulSoup(text, 'html.parser')
    item_list = soup.find('section', class_='box-panel result-search')
    item_list = item_list.find('div', class_='standart-view')
    item_list = item_list.find('div', id='searchResults')
    item_list = item_list.find_all('section', class_='ticket-item')
    return item_list


def pars_header(item_content):
    '''
    Dunction takes item content from html code
    Funcrion created for return header data and item url
    '''
    item_header = item_content.find('div', class_='head-ticket')  # header parse start here
    item_header = item_header.find('div', class_='item ticket-title')
    item_url = item_header.find('a', class_='address').get('href')  # get link
    item_header = item_header.find('span').getText()

    return item_header, item_url


def pars_item_basic_data(char_list):
    '''
    Function takes definition seller data.
    About mileage, location, transmission and fuel type
    Function created for division big code in get_item_description
    '''
    basic_data = {}

    for item_char in char_list:

        char_type = item_char.find('i').get('class')[0]
        if char_type == 'icon-mileage':
            basic_data['item_mileage'] = item_char.getText()

        elif char_type == 'icon-location':
            basic_data['item_location'] = item_char.getText()
        elif char_type == 'icon-fuel':
            basic_data['item_fuel_type'] = item_char.getText()
        elif char_type == 'icon-transmission':
            basic_data['item_transmission'] = item_char.getText()

    return basic_data


def pars_seller_description(item):
    '''
    Function takes item and return seller description text
    It's just seller description
    '''
    seller_description = item.find('p', class_='descriptions-ticket').find('span').getText()
    return seller_description


def pars_date(item):
    '''
    Function parse created data of current item
    '''
    date = item.find('div', class_='footer_ticket').find('span')
    created_date = date.get('data-add-date')
    update_date = date.get('data-update-date')
    return created_date, update_date


def get_seller_number(item_url):
    '''
    Function getting seller number from item_url
    '''
    request = get_html(item_url)

    soup = BeautifulSoup(request, 'html.parser')
    content = soup.find('main', class_='auto-content').find('div', class_='box-panel audit_3 dhide')
    number = content.find('div', class_='optionsset').find('a', class_='button-option').get('data-call')
    return number


# def get_comments():
#     '''
#      Function getting comments from item
#     '''
#     pass


def data(item_list):
    '''
    main function that include all data in the dictionary
    '''

    description = {}
    index = 0
    for item in item_list:
        description[f'{index}'] = {}
        item_content = item.find('div', class_='content-bar').find('div', class_='content')  # getting base page content

        item_header, item_url = pars_header(item_content)
        description[f'{index}']['item_header'] = item_header
        description[f'{index}']['item_url'] = item_url

        item_price = item_content.find('div', class_='price-ticket').get('data-main-price')  # get item price
        description[f'{index}']['item_price'] = item_price  # in price currency
        # see base_url
        item_definition_data = item_content.find('div', class_='definition-data')
        item_unstyle = item_definition_data \
            .find('ul', class_='unstyle characteristic').find_all('li')  # find basic data list

        description[f'{index}']['item_basic_data'] = pars_item_basic_data(item_unstyle)  # getting basic data

        description[f'{index}']['item_seller_description'] = pars_seller_description(
            item_definition_data)  # seller description

        created_date, update_date = pars_date(item_content)  # return created date and last update date

        description[f'{index}']['created_date'] = created_date
        description[f'{index}']['update_date'] = update_date

        # FIXME description[f'{index}']['parse_date'] = datetime.now()  # date and time of parsing the item

        description[f'{index}']['seller_number'] = get_seller_number(item_url)

        index += 1  # indexing all items

    return description


def main(category_id=1,
         price_currency=1,
         price_from=100,
         price_to=10000,
         location_id=11,
         brand_id=6,
         model_id=0,
         year_from=1900,
         year_to=2020):
    query = base_url.format(category_id,
                            price_currency,
                            price_from,
                            price_to,
                            location_id,
                            brand_id,
                            model_id,
                            year_from,
                            year_to)

    text = get_html(query)
    items = get_items(text)
    return data(items)
