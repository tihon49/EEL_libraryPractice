let table = document.querySelector('#agent_repair_table');
let contracts_table = document.querySelector('#all_contracts');
let agent_old_name;
let agent_id;


async function get_agent_data(){
    await eel.return_agent_name_to_agent_detail_js();
}
get_agent_data();


eel.expose(print_agent_data);
function print_agent_data(data){
    agent_old_name = data.name;
    agent_id = data.agent_id;

    let form = document.createElement('form');
    form.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 500px; text-align: center; margin-top: 0;" type="text" id="agent_name" required value="${agent_old_name}">`;

    let new_line = document.createElement('tr');
    let new_td = document.createElement('td');

    table.append(new_line);
    new_line.append(new_td);
    new_td.append(form);

    
    //отрисовка всех договоров контрагента
    for (contract of data.contracts) {
        let contract_number = contract.contract_number;
        let contract_description = contract.contract_description;

        let new_line = document.createElement('tr');
        contracts_table.append(new_line);

        let contract_number_TD = document.createElement('td');
        contract_number_TD.innerHTML = contract_number;
        new_line.append(contract_number_TD);

        let contract_description_TD = document.createElement('td');
        contract_description_TD.innerHTML = contract_description;
        new_line.append(contract_description_TD);

        //конопка редактировать
        let options_TD = document.createElement('td'),
            btn_options = document.createElement('button'),
            img_btn_options = document.createElement('img');

        options_TD.style = 'width: 105px; height: 50px;'
        btn_options.style = 'height: 33px; width: 33px;'
        img_btn_options.src = 'img/repair.svg';

        new_line.append(options_TD);
        options_TD.append(btn_options);
        btn_options.append(img_btn_options);

        //обработчик кнопки редактирования договора
        btn_options.addEventListener('click', function() {
            eel.update_contract_name(agent_id, contract_number);
        })


        //кнопка удалить
        let delete_TD = document.createElement('td'),
            btn_delete = document.createElement('button'),
            img_btn_delete = document.createElement('img');

        btn_delete.style = 'height: 33px; width: 33px;'
        img_btn_delete.src = 'img/trash.svg';

        new_line.append(delete_TD);
        delete_TD.append(btn_delete);
        btn_delete.append(img_btn_delete);

        //обраотчик кнопки удаления договора
        btn_delete.addEventListener('click', function() {
            // alert(`агент id: "${agent_id}" | номер договора: "${contract_number}"`)
            confirm_delete = confirm(`Вы действительно хотите удалить договор № "${contract_number}"?`);

            if (confirm_delete) {
                eel.contract_delete(agent_id, contract_number);
            }            
        })
    }
}


//кнопка сохранения изменений в имени контрагента
let btn_save = document.querySelector('#btn_save');
btn_save.addEventListener('click', function() {
    let agent_new_name = document.querySelector('#agent_name').value;

    confirm_alert = confirm(`Вы уверены что хотите переименовать контрагента "${agent_old_name}" на "${agent_new_name}"`);

    if (confirm_alert) {
        eel.update_agent_name(agent_old_name, agent_new_name);
    }
})


// функция перенаправления на страницу "agents_list.html"
eel.expose(redirect_to_agents_list);
function redirect_to_agents_list() {
    window.location = ('agents_list.html');
}


// функция обновления страницы
eel.expose(refresh_agent_detail);
function refresh_agent_detail() {
    window.location = ('agent_detail.html');
}


//функция перенаправления на страницу редактирования договора
eel.expose(redirect_to_contract_update_page);
function redirect_to_contract_update_page() {
    window.location = ('contract_update.html')
}