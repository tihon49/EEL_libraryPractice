let btn = document.querySelector('#btn_bill_register');
btn.addEventListener('click', add_bill);


// функция добавления счета к договору
async function add_bill() {
    let data = {'agent_name': document.querySelector('#agent_name').value,
                'contract_number': document.querySelector('#contract_number').value,
                'bill_number': document.querySelector('#bill_number').value,
                'bill_date': document.querySelector('#bill_date').value,
                'act_number': document.querySelector('#act_number').value,
                'act_date': document.querySelector('#act_date').value,
                'bill_sum': document.querySelector('#bill_sum').value,
                'act_sum': document.querySelector('#act_sum').value
    };

    // передача введенных на странице данных в функцию add_new_bill(data)
    await eel.add_new_bill(data);
}
