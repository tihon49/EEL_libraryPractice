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
        td_name.style = 'border: 1px solid #e8e8ec;';
        tr.append(td_name);

        let td_options = document.createElement('td'),
            option_btn = document.createElement('button'),
            img = document.createElement('img');

        td_options.style = 'border: 1px solid #e8e8ec;';
        option_btn.style = 'height: 33px; width: 33px; margin: 5px 20px';
        img.src = 'img/cogs.svg';
        option_btn.append(img);
        td_options.append(option_btn);
        tr.append(td_options);

        let agent_name = agent;
        option_btn.addEventListener('click', function() {
            // console.log(agent_name);
            eel.agent_from_all_agents(agent_name);
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


//TODO: кнопку "удалить"