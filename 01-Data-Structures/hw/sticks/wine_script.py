from collections import namedtuple


def parse_json_string(json_string):
    def decode_json(string):
        decoded_string = bytes(string, "utf-8").decode("unicode_escape")
        return decoded_string

    wine_dict_list = []
    wine_ntuple_list = []
    for wine_entry in json_string[3:-2].split('}, {"'):
        wine_dict = dict(
                        (k, decode_json(v.strip('"'))) 
                        for k, v in (item.split('": ')
                        for item in wine_entry.split(', "'))
                        )
        wine_dict_list.append(wine_dict)

    Wine = namedtuple('Wine', (wine_dict_list[0]))

    for wine_entry in wine_dict_list:
        wine = Wine(**wine_entry)
        wine_ntuple_list.append(wine)
    return wine_ntuple_list


def convert_symbols(string):
    return u''.join(char if 32 <= ord(char) <= 126 
                         else u'\\u%04x'%ord(char) for char in string)


def dump_json_string(wine_entry):
    #This function serves to create an output that completely
    #complies with the source formatting.
    wine_entry_to_string = '{'
    for field in wine_entry._fields:
        wine_entry_to_string += f'"{field}": '
        if getattr(wine_entry, field) == 'null':
            wine_entry_to_string += 'null, '
        elif field == 'price':
            wine_entry_to_string += str(getattr(wine_entry, field)) + ', '
        elif '"' in getattr(wine_entry, field):
            nonescaped_string = getattr(wine_entry, field)
            escaped_string = nonescaped_string.replace('"', '\\"')
            wine_entry_to_string += f'"{escaped_string}", '
        else:
            wine_entry_to_string += f'"{getattr(wine_entry, field)}", '

    complete_entry = convert_symbols(wine_entry_to_string[:-2]) + "}, "
    if r'\u000d\u000a' in complete_entry:
        complete_entry = complete_entry.replace(r'\u000d\u000a', r'\r\n')
    return complete_entry


def avarege_price(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    total_price = 0
    total_wines = 0
    for i in wine_list:
        if i.variety == variety and i.price != 'null':
            total_price += int(i.price)
            total_wines += 1
    return round(total_price/total_wines, 2)


def min_price(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    for i in reversed(wine_list):
        if i.variety == variety and i.price != 'null':
            lowest_price = int(i.price)
            break
    return lowest_price


def max_price(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    for i in wine_list:
        if i.variety == variety:
            highest_price = int(i.price)
            break
    return highest_price


def most_common_region(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    counting_dict = {}
    count = 0
    for i in wine_list:
        if i.region_1 != 'null' and i.variety == variety:
            counting_dict.setdefault(i.region_1, []).append(1)

    for name, values in counting_dict.items():
        if len(values) > count:
            count = len(values)
            region = name
    return region


def most_common_country(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    count = 0
    counting_dict = {}
    for i in wine_list:
        if i.country != 'null' and i.variety == variety:
            counting_dict.setdefault(i.country, []).append(1)

    for name, values in counting_dict.items():
        if len(values) > count:
            count = len(values)
            country = name
    return country


def avarage_score(wine_list, variety):
    if variety not in set([i.variety for i in wine_list]):
        return ('null')

    total_score = 0
    total_wines = 0
    for i in wine_list:
        if i.variety == variety and i.points != 'null':
            total_score += int(i.points)
            total_wines += 1
    return round(total_score/total_wines, 2)


def most_expensive_wine(wine_list):
    top_price = wine_list[0].price
    #Although there is only one wine with the maximum price,
    #this fucntion contains a loop for creating a list.
    #In order to avoid redundancy, this loop is not included in
    #other similar functions that return just one value.

    if wine_list[1].price != top_price:
        return wine_list[0].title
    else:
        expensive_wines = []
        for i in wine_list:
            if i.price == top_price:
                top_wines.append(i.title)
            else:
                break
        return sorted(expensive_wines)


def cheapest_wine(wine_list):
    cheap_wines = []
    low_price = min(int(i.price) for i in wine_list if i.price != 'null')

    for i in reversed(wine_list):
        if i.price == 'null':
            continue
        if int(i.price) == low_price:
            cheap_wines.append(i.title)
        else:
            break
    return sorted(cheap_wines)


def highest_score(wine_list):
    high_score = max([int(i.points) for i in wine_list])
    return high_score


def lowest_score(wine_list):
    low_score = min([int(i.points) for i in wine_list])
    return low_score


def most_expensive_coutry(wine_list):
    counting_dict = {}
    top_average = 0
    top_country = ''
    for i in wine_list:
        if i.country != 'null' and i.price != 'null':
            counting_dict.setdefault(i.country, []).append(int(i.price))

    for name, values in counting_dict.items():
        country_average = sum(values) / len(values)
        if country_average > top_average:
            top_country = name
            top_average = country_average
    return top_country


def cheapest_coutry(wine_list):
    counting_dict = {}
    low_average = 0
    low_country = ''
    for i in wine_list:
        if i.country != 'null' and i.price != 'null':
            counting_dict.setdefault(i.country, []).append(int(i.price))

    for name, values in counting_dict.items():
        country_average = sum(values) / len(values)
        if country_average > low_average and low_average == 0:
            low_average = country_average
            low_country = name
        elif country_average < low_average:
            low_average = country_average
            low_country = name
    return low_country


def most_rated_country(wine_list):
    counting_dict = {}
    top_average = 0
    top_country = ''
    for i in wine_list:
        if i.country != 'null' and i.points != 'null':
            counting_dict.setdefault(i.country, []).append(int(i.points))

    for name, values in counting_dict.items():
        country_average = sum(values) / len(values)
        if country_average > top_average:
            top_average = country_average
            top_country = name
    return top_country


def underrated_country(wine_list):
    counting_dict = {}
    low_average = 0
    low_country = ''
    for i in wine_list:
        if i.country != 'null' and i.points != 'null':
            counting_dict.setdefault(i.country, []).append(int(i.points))

    for name, values in counting_dict.items():
        country_average = sum(values) / len(values)
        if country_average > low_average and low_average == 0:
            low_average = country_average
            low_country = name
        elif country_average < low_average:
            low_average = country_average
            low_country = name
    return low_country


def most_active_commentator(wine_list):
    counting_dict = {}
    count = 0
    for i in wine_list:
        if i.taster_name != 'null':
            counting_dict.setdefault(i.taster_name, []).append(1)

    for name, values in counting_dict.items():
        if len(values) > count:
            count = len(values)
            commentator = name
    return commentator

with open('winedata_1.json') as f:
    raw_input = f.readline()
    wine_list_1 = parse_json_string(raw_input)

with open('winedata_2.json') as f:
    raw_input = f.readline()
    wine_list_2 = parse_json_string(raw_input)

wine_list = wine_list_1 + wine_list_2
wines_unique = list(dict.fromkeys(wine_list))
wines_out = sorted(sorted(wines_unique, key = lambda x : (x.variety)), 
                          key = lambda x : (int(x.price) if x.price.isdigit() 
                          else x.price == 'null'), reverse = True)

with open('winedata_full.json', 'w') as f:
    print("[", end = '', file = f)

    for i in wines_out[:-1]:
        entry = dump_json_string(i)
        print(entry, end = '', file = f)

    entry = dump_json_string(wines_out[-1])
    print(entry[:-2] + "]", end = '', file = f)

with open('stats.json', 'w') as f:
    #There are no entries with the 'Gewurztraminer' spelling.
    #Therefore the statistics is calculated for 'Gewürztraminer' only.
    requested = ['Gewürztraminer', 'Riesling', 'Merlot',
                'Madera', 'Tempranillo', 'Red Blend']

    print('{"statistics": {', file = f)
    print('\t\t"wine": {', file = f)

    for variety in requested:
        print(f'\t\t\t"{convert_symbols(variety)}"' + ': {', file = f)
        print('\t\t\t\t"avarege_price":',
              f'"{avarege_price(wines_out, variety)}", ', file = f)
        print('\t\t\t\t"min_price":',
              f'"{min_price(wines_out, variety)}", ', file = f)
        print('\t\t\t\t"max_price":',
              f'"{max_price(wines_out, variety)}", ', file = f)
        print('\t\t\t\t"most_common_region":',
              f'"{convert_symbols(most_common_region(wines_out, variety))}", ', file = f)
        print('\t\t\t\t"most_common_country":',
              f'"{most_common_country(wines_out, variety)}", ', file = f)
        print('\t\t\t\t"avarage_score":',
              f'"{avarage_score(wines_out, variety)}"', file = f)
        print('\t\t\t\t}', file = f)

    print('\t\t},', file = f)
    print('\t\t"most_expensive_wine":',
          f'"{convert_symbols(most_expensive_wine(wines_out))}",', file = f)   
    
    print('\t\t"cheapest_wine": [', file = f)
    for i in cheapest_wine(wines_out):
        if i != cheapest_wine(wines_out)[-1]:
            print('\t\t\t{' + f'"{convert_symbols(i)}"' + '}, ', file = f)
        else:
            print('\t\t\t{' + f'"{convert_symbols(i)}"' + '}', file = f)
            
    print('\t\t]', file = f)
    print('\t\t"highest_score":',
          f'"{highest_score(wines_out)}",', file = f)
    print('\t\t"lowest_score":',
          f'"{lowest_score(wines_out)}",', file = f)
    print('\t\t"most_expensive_coutry":',
          f'"{most_expensive_coutry(wines_out)}",', file = f)
    print('\t\t"cheapest_coutry":',
          f'"{cheapest_coutry(wines_out)}",', file = f)
    print('\t\t"most_rated_country":',
          f'"{most_rated_country(wines_out)}",', file = f)
    print('\t\t"underrated_country":',
          f'"{underrated_country(wines_out)}",', file = f)
    print('\t\t"most_active_commentator":',
          f'"{most_active_commentator(wines_out)}"', file = f)
    print('\t','}', file = f)
    print('}', end = '', file = f)