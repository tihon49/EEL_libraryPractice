let reg_btn = document.querySelector('#btn_agent_register');

// добавление нового контрагента
reg_btn.addEventListener('click', function() {
    let agent_name = document.querySelector('#agent_name').value;

    // передача питону введенных данных для валидации и записи в БД
    eel.add_new_agent(agent_name);
});
