from os import name
import re
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import eel
from pprint import pprint

from models import Agent, Contract, Bill, create_tables, delete_all_tables


engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()

eel.init('web')


def show_full_data():
    """Получаем полные данные по контрагентам"""

    query = session.query(Agent, Contract).filter(Agent.id == Contract.agent_id).order_by(Agent.id).all()
    return query


@eel.expose
def from_python() -> list:
    """
    данную функцию можно вызывать из js кода
    return: передает в js_функцию 'get_data()' данные из БД в виде списка 'data_list'
    """
    data = show_full_data()  # получаем все договоры из БД
    data_list = []

    # разбираем query на составляющие для последующей передачи в список
    # передавать будем словарь    
    for item in data:
        data_dict = {}

        data_dict['contract_number'] = item[1].number
        data_dict['agent_name'] = item[0].name
        data_dict['description'] = item[1].description
        data_dict['contract_sum'] = item[1].contract_sum
        data_dict['contract_balance'] = item[1].contract_balance
        data_dict['date_of_conclusion'] = item[1].date_of_conclusion.strftime('%d.%m.%Y')
        data_dict['date_of_start'] = item[1].date_of_start.strftime('%d.%m.%Y')
        data_dict['date_of_end'] = item[1].date_of_end.strftime('%d.%m.%Y')
        data_dict['validity'] = item[1].validity
        data_dict['days_passed'] = item[1].days_passed
        data_dict['days_left'] = item[1].days_left
        data_dict['state'] = item[1].state
        
        if data_dict['state'] and  data_dict['days_left'] > 0:
            data_dict['state'] = 'Активен'
        else:
            data_dict['state'] = 'Истек'
            data_dict['days_left'] = 0

        data_list.append(data_dict)

    # передаем список с данными в js функцию get_data() для отрисовки таблицы
    eel.get_data(data_list)


@eel.expose
def add_new_agent(agent_name):
    """валидация и запись нового контрагента в БД

    Args:
        agent_name (str): имя контрагента из формы на стр. agent_add.html
    """
    
    agent = session.query(Agent).filter_by(name=agent_name).all()

    # проверка на наличие контрагента в базе данных
    if agent:
        eel.alert_message(f'Контрагент "{agent[0].name}" уже сущесвует')
        print(f'Контрагент "{agent[0].name}" уже сущесвует')
        return False

    # валидация имени контрагента
    if agent_name:
        print(agent_name)
        new_agent = Agent(name=agent_name)
        session.add(new_agent)
        session.commit()
        new_agent_id = session.query(Agent).filter_by(name=agent_name).first().id
        eel.alert_message(f'Добавлен новый контрагент: {agent_name} c id: {new_agent_id}')
        print(f'Добавлен новый контрагент: {agent_name} c id: {new_agent_id}')
    else:
        eel.alert_message(f'Не верное имя агента: {agent_name}')
        print(f'Не верное имя агента: {agent_name}')
        return False
    return True


@eel.expose
def add_contract_into_db(data: dict):
    """
    Запись внесенных на странице contract_add.html данных в БД

    Args:
        data (dict): словарь с данными нового договора

    Returns:
        запись нового договора в БД
    """

    # проверка на заполнение всех полей
    for k, v in data.items():
        if not k or not v:
            print(f'параметр: {k} не заполнен')
            return False

    # валидадция введеного id агента
    agent_query = session.query(Agent).filter_by(name=data['agent_name']).all()
    if agent_query:
        agent_id = agent_query[0].id
        print(f'Выбран контрагент: {agent_query[0].name}, id: {agent_id}')
    else:
        print('Не вероно указано имя контрагента...\n')
        eel.alert_message('Не вероно указано имя контрагента...')
        return False

    # валидация номера договора
    contract_query = session.query(Contract).filter_by(agent_id=agent_id, number=data['number']).all()

    if contract_query:
        eel.alert_message(f'У контрагента {agent_query[0].name} уже есть договор № {contract_query[0].number}')
        print(f'У контрагента {agent_query[0].name} уже есть договор № {contract_query[0].number}')
        return False

    from datetime import date, datetime

    start_year = int(data['date_of_start'].split('.')[2])
    start_month = int(data['date_of_start'].split('.')[1])
    start_day = int(data['date_of_start'].split('.')[0])
    date_of_start = date(start_year, start_month, start_day)

    end_year = int(data['date_of_end'].split('.')[2])
    end_month = int(data['date_of_end'].split('.')[1])
    end_day = int(data['date_of_end'].split('.')[0])
    date_of_end = date(end_year, end_month, end_day)

    validity = (date_of_end - date_of_start).days
    now = datetime.now().date()
    days_passed = (now - date_of_start).days
    days_left = (date_of_end - now).days
        
    new_contract = Contract(agent_id = agent_id,
                            number = data['number'],
                            description = data['description'],
                            contract_sum = data['contract_sum'],
                            contract_balance = data['contract_sum'], 
                            date_of_conclusion = data['date_of_conclusion'],
                            date_of_start = data['date_of_start'],
                            date_of_end = data['date_of_end'],
                            validity = validity,
                            days_passed = days_passed,
                            days_left = days_left
    )

    session.add(new_contract)
    session.commit()
    eel.alert_message('Новый договор добавлен!')
    print('Новый договор добавлен!')
    return True


contract_detail_data = {}
@eel.expose
def get_agent_details(agent_name, contract_number):
    """после нажатия на кнопку детального отображения договора передаем в 
       словарь contract_detail_data данные по контракту в виде списка
    """
    # print(agent_name, contract_number)
    agent_id = session.query(Agent).filter_by(name=agent_name).first().id
    contract = session.query(Contract).filter_by(agent_id=agent_id, number=contract_number).first()
    contract_bills = []

    for bill in contract.bills:
        data = {'bill_number': bill.bill_number,
                'bill_sum': bill.bill_sum,
                'bill_date': bill.bill_date.strftime('%d.%m.%Y'),
                'act_number': bill.act_number,
                'act_sum': bill.act_sum,
                'act_date': bill.act_date.strftime('%d.%m.%Y')
        }
        contract_bills.append(data)

    # print(contract.number, agent_name, contract.bills)
    contract_detail_data['data'] = [contract.number, agent_name, contract_bills]


@eel.expose
def return_contract_detail_to_js():
    """передаем на js сторону список с данными по договору
       для отображения в таблице на странице
    """

    data = contract_detail_data['data']
    pprint(data)
    eel.print_contract_detail_data(data)


@eel.expose
def add_new_bill(data: dict):
    """валидация и добавление нового счета

    Args:
        data (dict): словарь с данными счета из bill_add.js 
    """

    # проверка на заполнение всех полей
    for k, v in data.items():
        if not v:
            eel.alert_message(f'параметр: {k} не заполнен')
            print(f'параметр: {k} не заполнен')
            return False

    # проверяем верно ли указан контрагент
    valid_agent = session.query(Agent).filter_by(name=data['agent_name']).first()

    if valid_agent:
        agent_id = int(valid_agent.id)
    else:
        eel.alert_message(f"Контрагент '{data['agent_name']}' отсутствует в базе данных")
        print(f"Контрагент '{data['agent_name']}' отсутствует в базе данных")
        return False

    # проверка валидности договора
    contract = session.query(Contract).filter_by(agent_id=agent_id, number=data['contract_number']).first()
    print(contract)

    if contract:
        # проверим вдруг счет с таким номером у данного договора уже есть
        bill_number = data['bill_number']

        if bill_number not in [b.bill_number for b in contract.bills]:
            bill_sum = int(data['bill_sum'])
            act_number = data['act_number']
            act_sum = int(data['act_sum'])
            bill_date = data['bill_date']
            act_date = data['act_date']

            new_bill = Bill(agent_id=agent_id, contract_number=data['contract_number'], bill_number=bill_number,
                            act_number=act_number, bill_sum=bill_sum, act_sum=act_sum, bill_date=bill_date,
                            act_date=act_date)
            contract.contract_balance -= bill_sum
            session.add(new_bill)
            session.commit()
    
            eel.alert_message(f'Счет {bill_number} успешно добавлен!')
            print(f'Счет {bill_number} успешно добавлен!')
            return True
        else:
            eel.alert_message('Данный счет уже есть в базе')
            print('Данный счет уже есть в базе')
    else:
        eel.alert_message(f"У контрагента {data['agent_name']} нет договора № {data['contract_number']}")
        print(f"У контрагента {data['agent_name']} нет договора № {data['contract_number']}")
    
    return False


# create_tables()
# delete_all_tables()
# from_python()

if __name__ == '__main__':
    eel.start('index.html', size=(1400, 600))
