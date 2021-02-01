# Программа для отслеживания состояний договоров

## Проект реализован на python библиотеке [Eel.](https://pypi.org/project/Eel/)

<br>

### Идея проекта была в реализации удобного интерфейса с необходимой логикой для внесения и ведения договоров с контрагентами, отслеживания сроков действия и баланса договоров, а так же исключения распространенных ошибок, например:
* повторное внесение одного и того же счета
* при ведении учета, например, в Excel таблицах, и удалении не верно внесенного счета могут "поехать" формулы, и тот же баланс договора расчитается не верно (да, я не верю Экселю :) )

<br>
Друними словами данная программа создана для упрощения ведения договоров с возможностью записи и редактирования следующих данных:

* контрагенты
* договоры
* счета

валидация данных и запись в базу данных ( PostgreSQL ) происходит автоматически.

<br>

### Второстепенная идея заключалась в простом интересе "поженить" Python и JavaScript, и сделать это НЕ с помощью Electorn.js

<br><hr><br>

### Главная страница
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/main.png/)

<br>

### Добавление нового договора
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/add_contract.png/)

<br>

### Добавить новый счет
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/add_bill.png/)

<br>

### Детальное отображение договора
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/contract_detail.png/)

<br>

### Список контрагентов
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/agents_list.png/)

<br>

### Детальное отображение контрагента
![Иллюстрация к проекту](https://github.com/tihon49/EEL_libraryPractice/blob/master/contracts/documentation_src/agent_detail.png/)

<br><hr><br>

### TODO: Проработать дизайн приложения
