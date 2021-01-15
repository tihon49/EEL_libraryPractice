// при загрузке страницы вызываем python функцию которая внутри себя
// получает актуальные данные по выбранному счету (из python функции "bill_detail")
// и вызывает JS функцию "print_bill_detail_data" с данными по счету
async function bill_detail() {
    await eel.return_bill_detail_to_js();
}
bill_detail();


// let table = document.querySelector('#bills_table'),
//     repeir_table = document.querySelector('#bills_repair_table');

let repeir_table = document.querySelector('#bills_repair_table');


// функция отрисовки DOM
eel.expose(print_bill_detail_data);
function print_bill_detail_data(data){
    // отрисовываем актуальные данные текущего счета
    // let tr = document.createElement('tr'),  //создаем строку в таблице (тег <tr>)
    //     td_bill_number = document.createElement('td'),
    //     td_bill_sum = document.createElement('td'),
    //     td_bill_date = document.createElement('td'),
    //     td_act_number = document.createElement('td'),
    //     td_act_sum = document.createElement('td'),
    //     td_act_date = document.createElement('td');

    // td_bill_number.innerHTML = data.bill_number;
    // td_bill_date.innerHTML = data.bill_date;
    // td_bill_sum.innerHTML = data.bill_sum;
    // td_act_number.innerHTML = data.act_number;
    // td_act_date.innerHTML = data.act_date;
    // td_act_sum.innerHTML = data.act_sum;

    // tr.append(td_bill_number);
    // tr.append(td_bill_date);
    // tr.append(td_bill_sum);
    // tr.append(td_act_number);
    // tr.append(td_act_date);
    // tr.append(td_act_sum);

    // table.append(tr);

    // форма изменения текущего счета
    let tr_repair = document.createElement('tr'),
        td_form_bill_number = document.createElement('td'),
        td_form_bill_date = document.createElement('td'),
        td_form_bill_sum = document.createElement('td'),
        td_form_act_number = document.createElement('td'),
        td_form_act_date = document.createElement('td'),
        td_form_act_sum = document.createElement('td');

    repeir_table.append(tr_repair);  // добавляем новую строку в таблице

    // формы
    let form_bill_number = document.createElement('form'); 
    form_bill_number.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center;" type="number" id="bill_number" required placeholder="Номер счета">';
    td_form_bill_number.append(form_bill_number);
    tr_repair.append(td_form_bill_number);

    let form_bill_date = document.createElement('form');
    form_bill_date.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 70px; text-align: center;" type="text" id="bill_date" required placeholder="Дата счета" value="11.12.1985">';
    td_form_bill_date.append(form_bill_date);
    tr_repair.append(td_form_bill_date);
    

    let form_bill_sum = document.createElement('form');
    form_bill_sum.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center;" type="number" id="bill_sum" required placeholder="Сумма счета" value="24000">';
    td_form_bill_sum.append(form_bill_sum);
    tr_repair.append(td_form_bill_sum);

    let form_act_number = document.createElement('form');
    form_act_number.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center;" type="number" id="bill_sum" required placeholder="Номер акта" value="1">';
    td_form_act_number.append(form_act_number);
    tr_repair.append(td_form_act_number);

    let form_act_date = document.createElement('form');
    form_act_date.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 70px; text-align: center;" type="text" id="bill_date" required placeholder="Дата акта" value="11.12.1985">';
    td_form_act_date.append(form_act_date);
    tr_repair.append(td_form_act_date);

    let form_act_sum = document.createElement('form');
    form_act_sum.innerHTML = '<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center;" type="number" id="bill_date" required placeholder="Сумма акта" value="24000">';
    td_form_act_sum.append(form_act_sum);
    tr_repair.append(td_form_act_sum);
}


//TODO: 1. Автозаполнение формы актуальными данными
//      2. При нажатии на кнопку "сохранить" сохранять изменеия в счете