import os

class Order:
    orders = []
    locations = {
            'г': ('по_городу', 130),
            'нг': ('нов.гор.', 280),
            'н': ('Невон', 250),
            'т': ('Тушама', 220),
            'л': ('ЛПК', 350),
            'в': ('Высотка', 190),
            'жд': ('Ж/Д', 440),
            'лс': ('Лесной', 430),
            }
    pay_types = {
            'н': 'наличные',
            'т': 'терминал',
            'о': 'оплачено',
            }
    
    def __init__(
            self,
            address,
            location,
            road_price,
            pay_type,
            price
            ) -> None:
        self.address = address
        self.location = location
        self.road_price = road_price
        self.pay_type = pay_type
        self.price = price

    def __str__(self) -> str:
        return f'''{self.address}, {self.location}, {self.pay_type}, {self.price}'''

    @classmethod
    def new_order(cls):
        address = input('Адрес: ').replace(' ', '_')
        location = input(
                '''Локация:
                по городу - г
                новый город - нг
                Невон - н
                ЛПК - л
                Тушама - т
                Высотка - в
                Лесной - лс
                '''
                )
        pay_type = input(
                '''Наличные, терминал, оплачено?
                н/т/о: '''
                )
        if pay_type == 'о':
            price = 0
        else:
            price = input('Стоимость: ')

        item = cls(
                address,
                cls.locations[location][0],
                cls.locations[location][1],
                cls.pay_types[pay_type],
                price
                )
        cls.orders.append(item)
        item.export_to_file()
        os.system('clear')
        print('Заказ добавлен.')

    def export_to_file(self):
        with open('orders.txt', 'a') as inp:
            print(
                    self.address,
                    self.location,
                    self.road_price,
                    self.pay_type,
                    self.price,
                    file=inp
                    )
    @classmethod
    def print_orders(cls):
        for num, item in enumerate(cls.orders, 1):
            print(f'{num}: {item}')

    @classmethod
    def reload_orders(cls):
        os.remove('orders.txt')
        for i in cls.orders:
            i.export_to_file()

    @classmethod
    def change_order(cls):
        cls.print_orders()
        try:
            index = int(input('Номер заказа: ')) - 1
            item = cls.orders[index]
            os.system('clear')
            while True:
                print(item)
                print(menues['order'])
                request = input()
                if request == 'з':
                    os.system('clear')
                    Order.reload_orders()
                    break
                elif request == 'т':
                    try:
                        new_pay_type = input('Тип оплаты: т/н/о ')
                        item.pay_type = Order.pay_types[new_pay_type]
                        if item.pay_type == 'оплачено':
                            item.price = 0
                    except KeyError:
                        print('Внимательней будь!')
                elif request == 'ц':
                    new_price = input('Новая цена: ')
                    item.price = new_price
                elif request == 'у':
                    confirm = input('Вы уверены? д/н ')
                    if confirm == 'д':
                        os.system('clear')
                        print('Заказ удален.')
                        Order.orders.remove(item)
                        Order.reload_orders()
                        break                
        except IndexError:
            print('Такой заказ не существует!')


    @classmethod
    def import_orders(cls):
        with open('orders.txt') as outp:
            for i in outp:
                items = i.strip().split()
                cls.orders.append(cls(*items))

    @classmethod
    def delete_orders(cls):
        cls.orders.clear()
        try:
            os.remove('orders.txt')
        except FileNotFoundError:
            pass

    @classmethod
    def calculate_shift(cls):
        orders_counter = len(cls.orders)
        total_money = sum(int(i.price) for i in cls.orders)
        cash = sum(int(i.price) for i in cls.orders if i.pay_type=='наличные')
        term = sum(int(i.price) for i in cls.orders if i.pay_type=='терминал')
        road = sum(int(i.road_price) for i in cls.orders)
        firm_money = cash - road
        paid = len(list(filter(lambda x: x.pay_type == 'оплачено', cls.orders)))
        print(f'''
        Всего заказов: {orders_counter}
        Общая сумма: {total_money}
        Оплаченные: {paid}
        Терминал: {term}
        Наличные: {cash}
        Дорога: {road}
        Нужно сдать: {firm_money}
        '''
        )

menues = {
        'main': '''
        ГЛАВНОЕ МЕНЮ:

        Новый заказ: н
        Изменить заказ: и
        Очистить список заказов: о
        Выход: в''',
        'order': '''
        МЕНЮ ЗАКАЗА:

        Изменить тип оплаты: т
        Изменить цену: ц
        Удалить заказ: у
        Завершить редактирование з'''
        }

responses = {
        'н': Order.new_order,
        'о': Order.delete_orders,
        'и': Order.change_order,
        }

def main():
    while True:
        Order.print_orders()
        Order.calculate_shift()
        print(menues['main'])
        request = input()
        if request == 'в':
            os.system('clear')
            break
        elif request == 'о':
            os.system('clear')
            print('Вы собираетесь удалить все заказы? д/н')
            confirm = input()
            if confirm == 'н':
                os.system('clear')
                continue
        os.system('clear')
        try:
            responses[request]()
        except KeyError:
            print('Некорректная команда!')


try:
    Order.import_orders()
except FileNotFoundError:
    pass

os.system('clear')
main()

