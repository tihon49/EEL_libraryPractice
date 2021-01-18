let table = document.querySelector('#agent_repair_table');


async function get_agent_data(){
    await eel.return_agent_name_to_agent_detail_js();
}
get_agent_data();


eel.expose(print_agent_data);
function print_agent_data(data){
    let form = document.createElement('form');
    form.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 100px; text-align: center;" type="text" id="bill_number" required value="${data}">`;

    let new_line = document.createElement('tr');
    let new_td = document.createElement('td');

    table.append(new_line);
    new_line.append(new_td);
    new_td.append(form);
}

// TODO: кнопку "сохранить"