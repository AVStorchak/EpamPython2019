import data_handler


a = {'name': 'Joe Doe', 'email': 'jd@example.com'}
data_handler.store('redis', 'pickle', a, 'pswd')
b = data_handler.get('redis', 'pickle', 'pswd')
print(b)

x = {'current_year': 2019, 'next_year': 2020}
data_handler.store('file', 'json', x, 'test.txt')
y = data_handler.get('file', 'json', 'test.txt')
print(y)
