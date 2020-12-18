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
        data_dict['date_of_conclusion'] = item[1].date_of_conclusion
        data_dict['date_of_start'] = item[1].date_of_start
        data_dict['date_of_end'] = item[1].date_of_end
        data_dict['validity'] = item[1].validity
        data_dict['days_passed'] = item[1].days_passed
        data_dict['days_left'] = item[1].days_left
        data_dict['state'] = item[1].state
        
        if data_dict['state']:
            data_dict['state'] = 'Активен'
        else:
            data_dict['state'] = 'Истек'

        data_list.append(data_dict)

    # передаем список с данными в js функцию get_data()
    eel.get_data(data_list)


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
        return False

    # валидация номера договора
    contract_query = session.query(Contract).filter_by(agent_id=agent_id, number=data['number']).all()

    if contract_query:
        print(f'У контрагента {agent_query[0]} уже есть договор {contract_query[0]}')
        return False
        
    new_contract = Contract(agent_id = agent_id,
                            number = data['number'],
                            description = data['description'],
                            contract_sum = data['contract_sum'],    
                            contract_balance = data['contract_balance'],
                            date_of_conclusion = data['date_of_conclusion'],
                            date_of_start = data['date_of_start'],
                            date_of_end = data['date_of_end'],
                            validity = data['validity'],
                            days_passed = data['days_passed'],
                            days_left = data['days_left']
    )

    session.add(new_contract)
    session.commit()
    print(f'Новый договор добавлен!')
    return True


@eel.expose
def add_new_agent(agent_name):
    """валидация и запись нового контрагента в БД

    Args:
        agent_name (str): имя контрагента из формы на стр. agent_add.html
    """
    
    agent = session.query(Agent).filter_by(name=agent_name).all()

    # проверка на наличие контрагента в базе данных
    if agent:
        print(agent[0], 'уже сущесвует.')
        return False

    # валидация имени контрагента
    if agent_name:
        print(agent_name)
        new_agent = Agent(name=agent_name)
        session.add(new_agent)
        session.commit()
        new_agent_id = session.query(Agent).filter_by(name=agent_name).first().id
        print(f'Добавлен новый контрагент: {agent_name} c id: {new_agent_id}')
    else:
        print(f'Не верное имя агента: {agent_name}')
        return False
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
                'bill_date': bill.bill_date,
                'act_number': bill.act_number,
                'act_sum': bill.act_sum,
                'act_date': bill.act_date
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
        data (dict): словарь с данными счета
    """

    # проверка на заполнение всех полей
    for k, v in data.items():
        if not k or not v:
            print(f'параметр: {k} не заполнен')
            return False

    # проверяем верно ли указан контрагента
    valid_agent = session.query(Agent).filter_by(name=data['agent_name']).first()

    if valid_agent:
        agent_id = int(valid_agent.id)
    else:
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
            session.add(new_bill)
            session.commit()
            print(f'Счет {bill_number} успешно добавлен!')
            return True
        else:
            print('Данный счет уже есть в базе')
    else:
        print(f"У контрагента {data['agent_name']} нет договора № {data['contract_number']}")
    
    return False


# create_tables()
# delete_all_tables()
# from_python()

if __name__ == '__main__':
    eel.start('index.html', size=(1400, 600))
