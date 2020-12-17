
// создаем листнер на конопке, по клику на которую вызывается 
// функция get_data_from_python()
// let btn = document.querySelector('#btn');
// btn.addEventListener('click', get_data_from_python);

// вызывает python функцию "from_python()"
async function get_data_from_python(){
    await eel.from_python();
}

get_data_from_python();


// эта функция вызывается из python кода, и получает данные из БД
// которые так же получаются в python коде
eel.expose(get_data);
function get_data(data){
    // Привязываемся к тегу таблицы
    let table = document.querySelector('table');

    // создаем стору tr и на основании полученных из функции (в питоне) from_python() данных
    // создаем переменные (разбираем полученные из data_list данные)
    for (let i=0; i<data.length; i++){
        let tr = document.createElement('tr')
        table.append(tr)

        let contract_number = data[i]['contract_number'],
            agent_name = data[i]['agent_name'],
            description = data[i]['description'],
            contract_sum = data[i]['contract_sum'],
            contract_balance = data[i]['contract_balance'],
            date_of_conclusion = data[i]['date_of_conclusion'],
            date_of_start = data[i]['date_of_start'],
            date_of_end = data[i]['date_of_end'],
            validity = data[i]['validity'],
            days_passed = data[i]['days_passed'],
            days_left = data[i]['days_left'],
            state = data[i]['state'];

        // создаем список со всеми созданными выше переменными
        let lst = [contract_number, agent_name, description, contract_sum, contract_balance,
                  date_of_conclusion, date_of_start, date_of_end, validity, days_passed,
                  days_left, state];

        // создаем переменную индекса на основании длинны полученного списка
        let td_index = document.createElement('th');
        td_index.style = 'border: 1px solid #000;';
        td_index.innerHTML = i + 1;
        tr.append(td_index);

        // заполняем таблицу данными в теги td передавая туда аргументы из списка lst
        for (let item = 0; item < lst.length; item++){
            let td = document.createElement('td');
            td.style = 'border: 1px solid #000;';
            td.innerHTML = lst[item];
            tr.append(td);
        }
    }
}