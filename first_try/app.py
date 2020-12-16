import eel
# https://www.youtube.com/watch?v=Iy6QFHzyi_4&t=7s

eel.init('web')

# данная функция будет вызываться в js коде
@eel.expose
def rec_data(login, password):
	print(f'Логин: {login}\nПароль: {password}')
	 
	# вызываем js функцию from_python и передаем
	# в нее аргумент data
	data = login + ' ' + password
	eel.from_python(data)


@eel.expose
def get_data_py():
	eel.get_data([i for i in range(10)])


eel.start('index.html', size=(500, 500))
