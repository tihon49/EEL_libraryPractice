let btn = document.querySelector('#btn_contract_register');
let choose_agent = document.querySelector('#agents_names');

async function main() {
    //имена всех контрагентов для удобного выбора
    let agents_list = await eel.all_agents()();
    console.log(agents_list);

    
    for (i of agents_list) {
        let option = document.createElement('option');
        option.innerHTML = `<option value="${i}"></option>`;
        choose_agent.append(option);
    }
}

main();

btn.addEventListener('click', function() {
    let agent_name = document.querySelector('#agent_name').value,
        number = document.querySelector('#number').value,
        contract_sum = document.querySelector('#contract_sum').value,
        date_of_conclusion = document.querySelector('#date_of_conclusion').value,
        date_of_start = document.querySelector('#date_of_start').value,
        date_of_end = document.querySelector('#date_of_end').value,
        description = document.querySelector('#description').value;
       
        data = {'agent_name': agent_name, 
                'number': number, 
                'description': description, 
                'contract_sum': contract_sum, 
                'date_of_conclusion': date_of_conclusion, 
                'date_of_start': date_of_start, 
                'date_of_end': date_of_end
            };
    eel.add_contract_into_db(data);
});
