let table = document.querySelector('#bills_table'),
    div_1 = document.querySelector('.cart_1'),
    div_2 = document.querySelector('.cart_2');


async function con_detail() {
    await eel.return_contract_detail_to_js();
}
con_detail();


// получаем из питона список с данными по счетам к выбранномму договору
// отрисовываем таблицу
eel.expose(print_contract_detail_data);
function print_contract_detail_data(data) {
    let h4 = document.createElement('h4'),
        agent_name = data[1];
    h4.innerHTML = agent_name;    
    div_1.append(h4)
        
    let h4_2 = document.createElement('h4'), 
        contract_number = data[0];
    h4_2.innerHTML = contract_number;
    div_2.append(h4_2)
    
    let data_list = data[2],
        index = 1;

    for (item of data_list) {
        let bill_number = item['bill_number'],
            bill_date = item['bill_date'],
            bill_sum = item['bill_sum'],
            act_number = item['act_number'],
            act_date = item['act_date'],
            act_sum = item['act_sum'];



        let tr = document.createElement('tr');
        table.append(tr);

        let index_th = document.createElement('th');
        index_th.innerHTML = index++;
        tr.append(index_th);

        let td_bill_number = document.createElement('td');
        td_bill_number.innerHTML = bill_number;
        tr.append(td_bill_number);

        let td_bill_date = document.createElement('td');
        td_bill_date.innerHTML = bill_date;
        tr.append(td_bill_date)

        let td_bill_sum = document.createElement('td');
        td_bill_sum.innerHTML = bill_sum;
        tr.append(td_bill_sum);

        let td_act_number = document.createElement('td');
        td_act_number.innerHTML = act_number;
        tr.append(td_act_number);

        let td_act_date = document.createElement('td');
        td_act_date.innerHTML = act_date;
        tr.append(td_act_date);

        let td_act_sum = document.createElement('td');
        td_act_sum.innerHTML = act_sum;
        tr.append(td_act_sum);     
        
        // кнопка редактирования счета
        let td_for_btn = document.createElement('td');
        td_for_btn.style = 'border: 1px solid #e8e8ec;';
        tr.append(td_for_btn);

        let td_btn = document.createElement('button'),
            img = document.createElement('img');

        td_btn.style = 'height: 33px; width: 33px; margin: 5px 20px';
        img.src = 'img/repair.svg';
        td_btn.appendChild(img);
        td_for_btn.append(td_btn);
        // TODO добавить окно редактирования счета


        // кнопка удаления счета
        let td_for_btn2 = document.createElement('td');
        td_for_btn2.style = 'border: 1px solid #e8e8ec;';
        tr.append(td_for_btn2);

        let td_btn2 = document.createElement('button'),
            img2 = document.createElement('img');

        td_btn2.style = 'height: 33px; width: 33px; margin: 5px 20px;';
        img2.src = 'img/trash.svg';
        td_btn2.appendChild(img2);
        td_for_btn2.append(td_btn2);

        // удаляем счет из БД
        td_btn2.addEventListener('click', function(){
            chouse = confirm('Вы уверенны что хотитие удалить счет?');

            if (chouse) {
                eel.bill_delete_python(contract_number, bill_number);  //удаляем счет из бд
                refresh_page_data(agent_name, contract_number);  // получаем обновленные данные по счетам из БД
            } 
        })
    }
}


// функция обновления страницы
eel.expose(refresh_contracts_detail);
function refresh_contracts_detail() {
    window.location = ('contract_detail.html');
}


// функция получения данных по договору из БД
async function refresh_page_data(agent_name, contract_number) {
    await eel.get_agent_details(agent_name, contract_number);
}
