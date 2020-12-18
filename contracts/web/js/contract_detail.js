let table = document.querySelector('#bills_table'),
    div = document.querySelector('#div_header');


async function con_detail() {
    await eel.return_contract_detail_to_js();
}
con_detail();


// получаем из питона список с данными по счетам к выбранномму договору
// отрисовываем таблицу
eel.expose(print_contract_detail_data);
function print_contract_detail_data(data) {
    let p = document.createElement('h4'),
        agent_name = data[1];
    p.innerHTML = 'Контрагент: ' + agent_name;    
    div.append(p)
        
    let p2 = document.createElement('h4'), 
        contract_number = data[0];
    p2.innerHTML = 'Номер договора: ' + contract_number;
    div.append(p2)
    
    let data_list = data[2];

    for (let i = 0; i < data_list.length; i++) {
        let tr = document.createElement('tr');
        table.append(tr);

        let index = document.createElement('th');
        index.innerHTML = i + 1;
        tr.append(index);

        let td_bill_number = document.createElement('td');
        td_bill_number.innerHTML = data_list[i].bill_number;
        tr.append(td_bill_number);

        let td_bill_date = document.createElement('td');
        td_bill_date.innerHTML = data_list[i].bill_date;
        tr.append(td_bill_date)

        let td_bill_sum = document.createElement('td');
        td_bill_sum.innerHTML = data_list[i].bill_sum;
        tr.append(td_bill_sum);

        let td_act_number = document.createElement('td');
        td_act_number.innerHTML = data_list[i].act_number;
        tr.append(td_act_number);

        let td_act_date = document.createElement('td');
        td_act_date.innerHTML = data_list[i].act_date;
        tr.append(td_act_date);

        let td_act_sum = document.createElement('td');
        td_act_sum.innerHTML = data_list[i].act_sum;
        tr.append(td_act_sum);        
    }
}