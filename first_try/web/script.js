// при на нажатии на кнопку #btn вызывается
// функция sendData
let btn = document.querySelector('#btn');
btn.addEventListener('click', sendData);

// описывавем функцию sendData
async function sendData(){
    let login = document.querySelector('#login').value;
    let password = document.querySelector('#password').value;

    // вызываем функцию из python кода и передаем ей
    // параметры: login и password
    await eel.rec_data(login, password);
    await eel.get_data_py();
}

// вызов js функции from_python в python коде
eel.expose(from_python); // аналог декоратора в python
function from_python(x) {
    console.log(x);
}

eel.expose(get_data);
function get_data(data){
    for (let i=0; i<data.length; i++) {
        let div = document.createElement('div');
        div.className = "alert";
        div.innerHTML = data[i];
        document.body.append(div);
    }
}
