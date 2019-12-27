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


def dump_json_string(wine_entry):
    wine_entry_to_string = '{'
    for field in wine_entry._fields:
        wine_entry_to_string += f'"{field}": '
        wine_entry_to_string += f'"{getattr(wine_entry, field)}", '

    complete_entry = wine_entry_to_string[:-2] + "}, "

    return complete_entry


def average_price(wine_list, variety):
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


def average_score(wine_list, variety):
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
wines_out = sorted(sorted(wines_unique, key=lambda x : (x.variety)),
                          key = lambda x : (int(x.price) if x.price.isdigit()
                          else x.price == 'null'), reverse = True)

with open('winedata_full.json', 'w', encoding="utf8") as f:
    print("[", end='', file=f)

    for i in wines_out[:-1]:
        entry = dump_json_string(i)
        print(entry, end='', file=f)

    entry = dump_json_string(wines_out[-1])
    print(entry[:-2] + "]", end='', file=f)

with open('stats.json', 'w', encoding="utf8") as f:
    #There are no entries with the 'Gewurztraminer' spelling.
    #Therefore the statistics is calculated for 'Gewürztraminer' only.
    requested_varieties = ['Gewürztraminer', 'Riesling', 'Merlot',
                           'Madera', 'Tempranillo', 'Red Blend']

    individual_parameters = [average_price, min_price, max_price,
                             most_common_region, most_common_country,
                             average_score]

    common_parameters = [most_expensive_wine, cheapest_wine, highest_score,
                         lowest_score, most_expensive_coutry, cheapest_coutry,
                         most_rated_country, underrated_country,
                         most_active_commentator]

    print('{"statistics": {', file=f)
    print('\t\t"wine": {', file=f)

    for variety in requested_varieties:
        entry_list = []

        for parameter in individual_parameters:
            entry = f'\t\t\t\t"{parameter.__name__}": ' + \
                    f'"{parameter(wines_out, variety)}"'
            entry_list.append(entry)

        exit_parameters = ", \n".join(entry_list)
        print(f'\t\t\t"{variety}"' + ': {\n' + exit_parameters +
              '\n\t\t\t\t}', file=f)

    print('\t\t},', file=f)

    entry_list = []

    for parameter in common_parameters:

        if isinstance(parameter(wines_out), list):
            output = '[\n\t\t\t{"' + '"} \n\t\t\t{"'.join([i for i in parameter(wines_out)]) + '"}\n\t\t]'
            entry = f'\t\t"{parameter.__name__}": ' + f'{output}'
            entry_list.append(entry)
            continue

        entry = f'\t\t"{parameter.__name__}": ' + f'"{parameter(wines_out)}"'
        entry_list.append(entry)

    exit_parameters = ", \n".join(entry_list)
    print(f'{exit_parameters}', file=f)

    print('\t', '}', file=f)
    print('}', end='', file=f)
