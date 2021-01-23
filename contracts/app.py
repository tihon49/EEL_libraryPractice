from os import name
import re
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import eel
from pprint import pprint
from datetime import date, datetime

from sqlalchemy.sql.expression import desc

from models import Agent, Contract, Bill, create_tables, delete_all_tables


engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()

eel.init('web')


def show_full_data():
    """Получаем полные данные по контрагентам"""

    #сортируем вывод договоров на главной странице
    query = session.query(Agent, Contract).filter(Agent.id == Contract.agent_id).order_by(
                                           Contract.state.desc()).order_by(
                                               Agent.name).order_by(
                                                   Contract.number).all()
    return query


@eel.expose
def get_agent_contracts(agent_name) -> list:
    """получаем все номера договоров выбрвнного контрагента"""

    try:
        agent = session.query(Agent).filter_by(name=agent_name).first()
        contracts = agent.contracts
        contracts_list = []

        for i in contracts:
            contracts_list.append(i.number)

        return contracts_list

    except:
        return None


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
        
        # получаем все счета данного контракта
        contract_bills_quey = session.query(Bill).filter_by(contract_number=item[1].number).all()
        bills_total_sum = 0

        # для корректного отображения баланса договора после редактирования или удаления
        # счета каждый раз высчитываем общую сумму счетов по договору
        for bill in contract_bills_quey:
            bills_total_sum += bill.bill_sum

        data_dict['contract_number'] = item[1].number
        data_dict['agent_name'] = item[0].name
        data_dict['description'] = item[1].description
        data_dict['contract_sum'] = item[1].contract_sum
        data_dict['contract_balance'] = item[1].contract_sum - bills_total_sum  #сумма договора минус сумма всех счетов договора
        data_dict['date_of_conclusion'] = item[1].date_of_conclusion.strftime('%d.%m.%Y')
        data_dict['date_of_start'] = item[1].date_of_start.strftime('%d.%m.%Y')
        data_dict['date_of_end'] = item[1].date_of_end.strftime('%d.%m.%Y')
        data_dict['validity'] = item[1].validity
        data_dict['days_passed'] = item[1].days_passed
        data_dict['days_left'] = item[1].days_left
        data_dict['state'] = item[1].state
        
        if data_dict['days_left'] > 0 and data_dict['contract_balance'] > 0:
            data_dict['state'] = 'Активен'
        elif data_dict['contract_balance'] <= 0:
            data_dict['state'] = 'Выбран'
            item[1].state = False
            session.commit()
        else:
            data_dict['state'] = 'Истек'
            data_dict['days_left'] = 0
            item[1].state = False
            session.commit()

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
    # pprint(data)
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
    # print(contract)

    if contract:
        # проверим вдруг счет с таким номером у данного договора уже есть
        bill_number = data['bill_number']

        if bill_number not in [b.bill_number for b in contract.bills]:
            bill_sum = float(data['bill_sum'])
            act_number = data['act_number']
            act_sum = float(data['act_sum'])
            bill_date = data['bill_date']
            act_date = data['act_date']

            new_bill = Bill(agent_id=agent_id, contract_number=data['contract_number'], bill_number=bill_number,
                            act_number=act_number, bill_sum=bill_sum, act_sum=act_sum, bill_date=bill_date,
                            act_date=act_date)
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


bill_detail_data = {}
@eel.expose
def bill_detail(contract_number, bill_number):
    """
    редактирование счета

    получаем из JS данные contract_number, bill_number.
    делаем запрос к БД

    полученные данные кладем в глобальную переменную "bill_detail_data" чтобы потом в JS коде можно было вызвать функцию
    отрисовки DOM страницы с полученными из глобальной переменной "bill_detail_data" данными
    """
    global bill_detail_data
    bill = session.query(Bill).filter_by(contract_number=contract_number, bill_number=bill_number).first()
    data = {'agent_id': bill.agent_id,
            'contract_number': bill.contract_number,
            'bill_number': bill.bill_number,
            'bill_sum': bill.bill_sum,
            'bill_date': bill.bill_date.strftime('%d.%m.%Y'),
            'act_number': bill.act_number,
            'act_sum': bill.act_sum,
            'act_date': bill.act_date.strftime('%d.%m.%Y')
    }
    bill_detail_data = data


@eel.expose
def bill_updated_data(data):
    """
    обновление даныых счета ("bill_detail.html")
    """

    contract_number = data[0]  #эти данные нужны для корректного запроса к базе данных
    bill_old_number = data[1]  #така они составляют PrimaryKeyConstraint модели Bill

    bill_new_number = data[2]
    bill_date = data[3]
    bill_sum = data[4]
    act_number = data[5]
    act_date = data[6]
    act_sum = data[7]
    agent_id = data[8]

    bill = session.query(Bill).filter_by(contract_number=contract_number, bill_number=bill_old_number).first()
    agent_name = session.query(Agent).filter_by(id=agent_id).first().name
    
    bill.bill_number = bill_new_number
    bill.bill_date = bill_date
    bill.bill_sum = bill_sum
    bill.act_number = act_number
    bill.act_date = act_date
    bill.act_sum = act_sum

    session.commit()
    # print(f'Имя контрагента: {agent_name}, номер договора: {contract_number}')
    get_agent_details(agent_name, contract_number)
    eel.refresh_contracts_detail()


@eel.expose
def return_bill_detail_to_js():
    """
    функция для вызова из JS кода со страницы "bill_detail.html"
    передаст в JS данные из глобальной переменной "bill_detail_data" для последующей отрисовки DOM
    """

    data = bill_detail_data
    eel.print_bill_detail_data(data)


@eel.expose
def bill_delete_python(contract_number, bill_number):
    """удаление счета"""

    bill = session.query(Bill).filter_by(contract_number=contract_number, bill_number=bill_number).first()
    # print(bill)
    session.delete(bill)
    session.commit()
    print(f'Счет №{bill.bill_number} удален из базы данных.')
    eel.alert_message(f'Счет №{bill.bill_number} удален из базы данных.')
    eel.refresh_contracts_detail()  #обновление страницы
    

@eel.expose
def all_agents() -> list:
    """получение списка имен всех контрагентов"""

    query = session.query(Agent).all()
    agents_list = []

    for agent in query:
        agents_list.append(agent.name)

    return agents_list


agent_from_all_agents_list = {}
def refresh_contracts_list(agent):
    global agent_from_all_agents_list

    all_contracts = agent.contracts
    contracts_list = []
    for contract in all_contracts:
        contracts_list.append({'contract_number': contract.number,
                               'contract_description': contract.description})
    
    return contracts_list


@eel.expose
def agent_from_all_agents(agent_name):
    """
    выбираем контрагента со страницы "agaents_list.html"
    """

    global agent_from_all_agents_list

    agent = session.query(Agent).filter_by(name=agent_name).first()
    agent_from_all_agents_list['name'] = agent.name
    agent_from_all_agents_list['agent_id'] = agent.id
    agent_from_all_agents_list['contracts'] = refresh_contracts_list(agent)
    
    eel.redirect_to_agent_detail_page()


@eel.expose
def return_agent_name_to_agent_detail_js():
    eel.print_agent_data(agent_from_all_agents_list)


@eel.expose
def agent_delete(agent_name):
    agent = session.query(Agent).filter_by(name=agent_name).first()
    session.delete(agent)
    session.commit()
    
    # print(f'{agent} удален из БД')
    eel.refresh_agents_list_page()


@eel.expose 
def update_agent_name(agent_old_name, agent_new_name):
    """Изменение имени контрагента при нажатии на кнопку "Сохранить"
       на страницу "agent_detail.html"
    """

    agent = session.query(Agent).filter_by(name=agent_old_name).first()
    agent.name = agent_new_name
    session.commit()
    eel.redirect_to_agents_list()


@eel.expose
def contract_delete(agent_id, contract_number):
    """
    удаление договора на странице "agent_detail.html"
    при нажатии на кнопку "удалить"
    """

    contract = session.query(Contract).filter_by(agent_id=agent_id, number=contract_number).first()
    session.delete(contract)
    session.commit()

    global agent_from_all_agents_list

    agent = session.query(Agent).filter_by(id=agent_id).first()
    agent_from_all_agents_list['contracts'] = refresh_contracts_list(agent)
    eel.refresh_agent_detail()


contract_update_data = {}
@eel.expose
def update_coontract_name(agent_id, contract_number):
    """
    функция обновления данных договора
    получаем данные контракта, перенаправляем на страницу редактирования контракта
    """
    
    global contract_update_data
    contract = session.query(Contract).filter_by(agent_id=agent_id, number=contract_number).first()
    contract_update_data = {'agent_id': agent_id,
                            'agent_name': contract.agent.name,
                            'contract_number': contract.number,
                            'description': contract.description,
                            'contract_sum': contract.contract_sum,
                            'date_of_conclusion': contract.date_of_conclusion.strftime('%d.%m.%Y'),
                            'date_of_start': contract.date_of_start.strftime('%d.%m.%Y'),
                            'date_of_end': contract.date_of_end.strftime('%d.%m.%Y'),
                            'state': contract.state}
 
    eel.redirect_to_contract_update_page()


@eel.expose
def get_contract_update_data():
    """для получения словаря 'contract_update_data' в JS коде"""
    return contract_update_data
    

@eel.expose
def update_contract_data(data: list):
    """обновление данных контракта"""

    agent_id = data[0]
    contract_old_number = data[1]
    contract_new_number = data[2]
    description = data[3]
    contract_sum = data[4]
    date_of_conclusion = data[5]
    date_of_start = data[6]
    date_of_end = data[7]
    # state = data[8]

    start_year = int(date_of_start.split('.')[2])
    start_month = int(date_of_start.split('.')[1])
    start_day = int(date_of_start.split('.')[0])
    date_of_start = date(start_year, start_month, start_day)

    end_year = int(date_of_end.split('.')[2])
    end_month = int(date_of_end.split('.')[1])
    end_day = int(date_of_end.split('.')[0])
    date_of_end = date(end_year, end_month, end_day)

    validity = (date_of_end - date_of_start).days
    now = datetime.now().date()
    days_passed = (now - date_of_start).days
    days_left = (date_of_end - now).days

    contract = session.query(Contract).filter_by(agent_id=agent_id, number=contract_old_number).first()
     
    contract.number = contract_new_number
    contract.description = description
    contract.contract_sum = contract_sum
    contract.date_of_conclusion = date_of_conclusion
    contract.date_of_start = date_of_start.strftime('%d.%m.%Y')
    contract.date_of_end = date_of_end.strftime('%d.%m.%Y')
    contract.validity = validity
    contract.days_passed = days_passed
    contract.days_left = days_left
    # contract.state = state

    session.commit()

    global agent_from_all_agents_list

    agent = session.query(Agent).filter_by(id=agent_id).first()
    agent_from_all_agents_list['contracts'] = refresh_contracts_list(agent)

    eel.redirect_to_agent_detail_page()



# create_tables()
# delete_all_tables()
# from_python()


if __name__ == '__main__':
    eel.start('index.html', size=(1400, 700))
