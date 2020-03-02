from static_data import locations, brands
from pars_data import main

# def get_model_ids():
#     '''
#     Fucking ugly site, doesnt give json normaly. Fine. I give this by hands (sorry)
#     Return json file with many interesting parameter:
#     Item search id's, country search id's and many. If you want, give this response
#     in file and see.
#     Ok, this file is 'parameters'
#     '''

def intro():
    print('#' * 40)
    print('Hello my friend! \n'
          'This is AutoRia parser. \n'
          'you can use this for you solutions \n'
          'all information: <GitHub.com/blablabla>')
    print('#' * 40)


def choice_brand():
    base_models = brands['base']
    popular_models = brands['popular']

    text = 'Popular models \n'
    counter = 0  # def counter for imagination 3 columns
    for key in popular_models['1']:
        model_id = base_models[f'{key}']['value']
        model_name = base_models[f'{key}']['name']
        text += '[{0}]  {1}  '.format(model_id, model_name)
        counter += 1

        if counter == 3:
            text += '\n'
            counter = 0
    return text


def choice_model():
    pass


def choice_location():
    text = ''
    counter = 0 # def counter for imagination 3 columns
    for key in locations['centers']:
        loc_id = key
        loc_name = locations['centers'][key]['name']
        text += '[{0}]  {1}'.format(loc_id, loc_name)
        counter += 1

        if counter == 3:
            text += '\n'
            counter = 0
    return text


def create_file(file_format, data):
    pass


def check_parameters(params):
    pass


def main():
    #TODO:
    # category_id = '1'  # легковые format 0 -- DONE
    # price_currency = '1'  # USD   format 1 -- DONE
    # price_from = '100'  # format 2         -- DONE
    # price_to = '10000'  # format 3         -- DONE
    # region_id = '10'  # Kyiv  format 4     -- DONE
    # brand_id = '6'  # Audi  format 5       -- DONE
    # model_id = '39'  # 100   format 6      ??????
    # year_from = '1990'  # format 7         -- DONE
    # year_to = '2020'  # format 8           -- DONE

    #TODO:
    # file export format: json, csv
    # work with text imagination in terminal
    # ((([84]  Volkswagen  [48]  Mercedes-Benz  [88]  ВАЗ
    # [79]  Toyota  [70]  Skoda  [62]  Renault
    # [9]  BMW  [6]  Audi  [24]  Ford
    # [56]  Opel  [29]  Hyundai  [55]  Nissan
    # [33]  Kia  [52]  Mitsubishi  [13]  Chevrolet
    # [47]  Mazda  [28]  Honda  [18]  Daewoo
    # [89]  ЗАЗ  [58]  Peugeot)))  ==>  that is not OK!!!


    intro()
    print('Now, we enter some parameter, if you dont want to use any parameter, just enter "pass"')
    user_parameters = []
    while True:  # main loop
        print(choice_brand())  # text of popular brands.
        brand_id = int(input('Choice from popular brand (all model list on GitHub)\n brand id: '))
        user_parameters.append(brand_id)
        if brand_id in brands['popular']['1']:
            break
        else:
            print('Error: Please, choice available model from list')
    while True:
        print(choice_location())  # text of available locations
        location_id = input('Choice location of search\n location id: ')
        user_parameters.append(location_id)
        if location_id in locations['centers'].keys():
            break
        else:
            print('Error: Please enter location id from list')
    while True:
        print('Please enter price from - to in $')
        try:
            price_from = int(input('From: $'))
            price_to = int(input('To: $'))
            user_parameters.append(price_from)
            user_parameters.append(price_to)
            break
        except ValueError:
            print('Error: Please enter valid number without spaces')
    while True:
        print('Please enter year from - to')
        year_from = int(input('From: '))
        year_to = int(input('To: '))
        user_parameters.append(year_from)
        user_parameters.append(year_to)
        if 1900 < year_from < 2021 and 1900 < year_to < 2021:
            break
        else:
            print('Error: Please use range 1900 to 2021')

    while True:
        print('All parameter correct?')
        #print(check_parameters(params=123))
        print(user_parameters)
        answr = input('y/n')
        if answr == 'y':
            print('OK')
            break
        else:
            print('Abort from user')
            print(brand_id)
            break
        data = main(
                brand_id=brand_id,
                location_id=location_id,
                price_from=price_from,
                price_to=price_to,
                year_from=year_from,
                year_to=year_to)

        print('[1] JSON\n [2] CSV\n [3] Print to console\n [4] Text file (will create)')
        file_format = input('Choice file format: ')
        if file_format in '124':
            print('Processing')
            create_file(file_format=file_format, data=data)
            break
        elif file_format == '3':
            print(data)
            break


if __name__ == '__main__':
    main()
