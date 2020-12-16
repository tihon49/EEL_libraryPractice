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

    # разюираем query на составляющие для последующей передачи в список
    for item in data:
        contract_number = item[1].number
        agent_name = item[0].name
        description = item[1].description
        contract_sum = item[1].contract_sum
        contract_balance = item[1].contract_balance
        date_of_conclusion = item[1].date_of_conclusion
        date_of_start = item[1].date_of_start
        date_of_end = item[1].date_of_end
        validity = item[1].validity
        days_passed = item[1].days_passed
        days_left = item[1].days_left
        state = item[1].state
        
        if state:
            state = 'Активен'
        else:
            state = 'Истек'

        data_list.append([contract_number, agent_name, description, contract_sum, contract_balance,
                        date_of_conclusion, date_of_start, date_of_end, validity,
                        days_passed, days_left, state])

    # передаем список с данными в js функцию get_data()
    eel.get_data(data_list)


# create_tables()
# delete_all_tables()
# from_python()

if __name__ == '__main__':
    eel.start('index.html')
