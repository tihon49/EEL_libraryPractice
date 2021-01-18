let table = document.querySelector('#agent_repair_table');
let agent_old_name;


async function get_agent_data(){
    await eel.return_agent_name_to_agent_detail_js();
}
get_agent_data();


eel.expose(print_agent_data);
function print_agent_data(data){
    agent_old_name = data;

    let form = document.createElement('form');
    form.innerHTML = `<input style="background-color: rgb(248, 248, 231); width: 800px; text-align: center;" type="text" id="agent_name" required value="${data}">`;

    let new_line = document.createElement('tr');
    let new_td = document.createElement('td');

    table.append(new_line);
    new_line.append(new_td);
    new_td.append(form);
}

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