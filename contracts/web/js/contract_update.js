let table = document.querySelector('#contract_repare_table');
let h3_agent_name = document.querySelector('#agent_name');
let agent_id;
let contract_old_number;


async function main() {
    let data = await eel.get_contract_update_data()();
    console.log(data);

    h3_agent_name.innerHTML = data.agent_name;
    agent_id = data.agent_id;
    contract_old_number = data.contract_number;

    let new_line = document.createElement('tr');
    table.append(new_line);

    //номер договора
    let contract_number_TD = document.createElement('td');
    new_line.append(contract_number_TD);

    let contract_number_FORM = document.createElement('form');
    contract_number_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="text" id="contract_number" required value="${data.contract_number}">`;
    contract_number_TD.append(contract_number_FORM);

    //описание договора
    let description_TD = document.createElement('td');
    new_line.append(description_TD);

    let description_FORM = document.createElement('form');
    description_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="text" id="contract_description" required value="${data.description}">`;
    description_TD.append(description_FORM);

    //сумма договора
    let con_sum_TD = document.createElement('td');
    new_line.append(con_sum_TD);

    let con_sum_FORM = document.createElement('form');
    con_sum_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="number" id="contract_sum" required value="${data.contract_sum}">`;
    con_sum_TD.append(con_sum_FORM);

    //дата заключения договора
    let con_date_conclusion_TD = document.createElement('td');
    new_line.append(con_date_conclusion_TD);

    let con_date_conclusion_FORM = document.createElement('form');
    con_date_conclusion_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="text" id="date_of_conclusion" required value="${data.date_of_conclusion}">`;
    con_date_conclusion_TD.append(con_date_conclusion_FORM);

    //дата начала
    let con_start_date_TD = document.createElement('td');
    new_line.append(con_start_date_TD);

    let con_start_date_FORM = document.createElement('form');
    con_start_date_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="text" id="date_of_start" required value="${data.date_of_start}">`;
    con_start_date_TD.append(con_start_date_FORM);

    //дата окончания
    let date_end_TD = document.createElement('td');
    new_line.append(date_end_TD);

    let date_end_FORM = document.createElement('form');
    date_end_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 0;" type="text" id="date_of_end" required value="${data.date_of_end}">`;
    date_end_TD.append(date_end_FORM);

    //состояние
    let state_TD = document.createElement('td');
    new_line.append(state_TD);

    let state_FORM = document.createElement('form');
    if (data.state) {
        state_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 5px;" type="text" id="state" required value="Действует">`;
    } else {
        state_FORM.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center; margin-top: 5px;" type="text" id="state" required value="Истек">`;
    }
    state_TD.append(state_FORM);
}

main();

//кнопка сохранит изменения
let btn_save = document.querySelector('#btn_save');
btn_save.addEventListener('click', function() {
    let contract_new_number = document.querySelector('#contract_number').value,
        description = document.querySelector('#contract_description').value,
        contract_sum = document.querySelector('#contract_sum').value,
        date_of_conclusion = document.querySelector('#date_of_conclusion').value,
        date_of_start = document.querySelector('#date_of_start').value,
        date_of_end = document.querySelector('#date_of_end').value,
        state = document.querySelector('#state').value;

    let data_list = [agent_id, contract_old_number, contract_new_number, description, 
                    contract_sum, date_of_conclusion, date_of_start, date_of_end, state];

    send_contract_data_to_python(data_list);
})

//передача новых данных договора в питон
async function send_contract_data_to_python(data) {
    await eel.update_contract_data(data);
}

//функция перенаправления на страницу "agent_detail.html"
eel.expose(redirect_to_agent_detail_page);
function redirect_to_agent_detail_page() {
    window.location = ('agent_detail.html')
}