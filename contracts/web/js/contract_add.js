let btn = document.querySelector('#btn_contract_register');
btn.addEventListener('click', foo);


async function foo() {
    let agent_name = document.querySelector('#agent_name').value,
        number = document.querySelector('#number').value,
        contract_sum = document.querySelector('#contract_sum').value,
        contract_balance = document.querySelector('#contract_balance').value,
        date_of_conclusion = document.querySelector('#date_of_conclusion').value,
        date_of_start = document.querySelector('#date_of_start').value,
        date_of_end = document.querySelector('#date_of_end').value,
        validity = document.querySelector('#validity').value,
        days_passed = document.querySelector('#days_passed').value,
        days_left = document.querySelector('#days_left').value,
        description = document.querySelector('#description').value;
       
        data = {'agent_name': agent_name, 
                'number': number, 
                'description': description, 
                'contract_sum': contract_sum, 
                'contract_balance': contract_balance, 
                'date_of_conclusion': date_of_conclusion, 
                'date_of_start': date_of_start, 
                'date_of_end': date_of_end, 
                'validity': validity, 
                'days_passed': days_passed, 
                'days_left': days_left
            };
    await eel.add_contract_into_db(data);
};