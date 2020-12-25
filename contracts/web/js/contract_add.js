let btn = document.querySelector('#btn_contract_register');

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
