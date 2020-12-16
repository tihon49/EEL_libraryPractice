
// создаем листнер на конопке, по клику на которую вызывается 
// функция get_data_from_python()
let btn = document.querySelector('#btn');
btn.addEventListener('click', get_data_from_python);

// вызывает python функцию "from_python()"
async function get_data_from_python(){
    await eel.from_python();
}


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

        let contract_number = data[i][0],
            agent_name = data[i][1],
            description = data[i][2],
            contract_sum = data[i][3],
            contract_balance = data[i][4],
            date_of_conclusion = data[i][5],
            date_of_start = data[i][6],
            date_of_end = data[i][7],
            validity = data[i][8],
            days_passed = data[i][9],
            days_left = data[i][10],
            state = data[i][11];

        // создаем список со всеми созданными выше переменными
        let lst = [contract_number, agent_name, description, contract_sum, contract_balance,
                  date_of_conclusion, date_of_start, date_of_end, validity, days_passed,
                  days_left, state];

        // создаем переменную индекса на основании длинны полученного списка
        let td_index = document.createElement('td');
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