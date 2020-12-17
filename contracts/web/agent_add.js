let reg_btn = document.querySelector('#btn_agent_register');
reg_btn.addEventListener('click', add_agent);


// добавление нового контрагента
async function add_agent() {
    let agent_name = document.querySelector('#agent_name').value;

    // передача питону введенных данных для валидации и записи в БД
    await eel.add_new_agent(agent_name);
}