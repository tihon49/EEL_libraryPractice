async function show_all_agents() {
    let agents_list = await eel.all_agents()(),
        table = document.querySelector('.agents__table_body'),
        index = 1;

    for (agent of agents_list) {
        let tr = document.createElement('tr');
        table.append(tr);

        let td_index = document.createElement('td');
        td_index.innerHTML = index;
        td_index.style = 'border: 1px solid #e8e8ec;';
        tr.append(td_index);

        let td_name = document.createElement('td');
        td_name.innerHTML = agent;
        td_name.style = 'border: 1px solid #e8e8ec; width: 200px;';
        tr.append(td_name);

        let td_options = document.createElement('td'),
            option_btn = document.createElement('button'),
            img_options = document.createElement('img');

        td_options.style = 'border: 1px solid #e8e8ec;';
        option_btn.style = 'height: 33px; width: 33px; margin: 5px 20px';
        img_options.src = 'img/cogs.svg';
        option_btn.append(img_options);
        td_options.append(option_btn);
        tr.append(td_options);


        let td_delete = document.createElement('td'),
            delete_btn = document.createElement('button'),
            img_delete = document.createElement('img');

        td_delete.style = 'border: 1px solid #e8e8ec;';
        delete_btn.style = 'height: 33px; width: 33px; margin: 5px 20px';
        img_delete.src = 'img/trash.svg';
        delete_btn.append(img_delete);
        td_delete.append(delete_btn);
        tr.append(td_delete);


        let agent_name = agent;
        option_btn.addEventListener('click', function() {
            // console.log(agent_name);
            eel.agent_from_all_agents(agent_name);
        });

        delete_btn.addEventListener('click', function() {
            chouse_to_delete = confirm(`Вы действительно хотите удалить контрагена "${agent_name}"`);

            if (chouse_to_delete) {
                alert(`Контрагент "${agent_name}" удален из БД`);
                eel.agent_delete(agent_name);
            }
        });

        index++;
    };
}

show_all_agents();

// функция перенаправления на страницу редактирования контрагента
eel.expose(redirect_to_agent_detail_page);
function redirect_to_agent_detail_page() {
    window.location = ('agent_detail.html');
}


// функция обновления страницы
eel.expose(refresh_agents_list_page);
function refresh_agents_list_page() {
    window.location = ('agents_list.html');
}