// Заполнение списка курсов на основе данных из сервера
function fillCourseList() {
    fetch('/lab8/api/courses/')
        .then(function (data) {
            return data.json();
        })
        .then(function (courses) {
            let tbody = document.getElementById('course-list');
            tbody.innerHTML = '';
            for (let i = 0; i < courses.length; i++) {
                // Создание строк таблицы для каждого курса
                let tr = document.createElement('tr');

                // Создание ячеек для имени, количества видео, цены и даты создания курса
                let tdName = document.createElement('td');
                tdName.innerText = courses[i].name;

                let tdVideos = document.createElement('td');
                tdVideos.innerText = courses[i].videos;

                let tdPrice = document.createElement('td');
                tdPrice.innerText = courses[i].price !== undefined ? courses[i].price : 'бесплатно';

                let tdDATA = document.createElement('td');
                let serverDate = new Date(courses[i].createdAt);
                let localDate = new Date(serverDate.getTime() + serverDate.getTimezoneOffset() * 60000);
                tdDATA.innerText = localDate.toLocaleDateString();

                // Создание кнопок для редактирования и удаления курса
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editCourse(i, courses[i]);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteCourse(i);
                };

                let tdActions = document.createElement('td');
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавление ячеек в строку и строки в таблицу
                tr.append(tdName);
                tr.append(tdVideos);
                tr.append(tdPrice);
                tr.append(tdActions);
                tr.append(tdDATA);
                tbody.append(tr);
            }
        });
}

// Удаление курса с подтверждением от пользователя
function deleteCourse(num) {
    if (!confirm('Вы точно хотите удалить курс?')) {
        return;
    }

    // Выполнение запроса на удаление курса
    fetch('/lab8/api/courses/' + num, { method: 'DELETE' })
        .then(function () {
            // После успешного удаления, обновить список курсов
            fillCourseList();
        })
        .catch(function (error) {
            console.error('Ошибка при удалении курса:', error);
        });
}

// Отображение модального окна
function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

// Скрытие модального окна
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

// Отмена операции (закрытие модального окна)
function cancel() {
    hideModal();
}

// Добавление нового курса (открытие модального окна)
function addCourse() {
    const course = {};
    delete course.createdAt;
    document.getElementById('num').value = '';
    document.getElementById('name').value = '';
    document.getElementById('videos').value = '';
    document.getElementById('price').value = '';
    showModal();
}

// Отправка данных о курсе на сервер
function sendCourse() {
    const num = document.getElementById('num').value;
    const name = document.getElementById('name').value;
    const videos = document.getElementById('videos').value;
    const price = document.getElementById('price').value;

    // Проверка, если цена 0, установить значение 'бесплатно'
    const normalizedPrice = price === '0' ? 'бесплатно' : price;

    // Проверка наличия имени и количества видео
    if (!name || !videos) {
        alert('Заполните все поля!');
        return;
    }

    // Формирование объекта курса для отправки на сервер
    const course = {
        name: name,
        videos: videos,
        price: normalizedPrice,
    };

    // Определение URL и метода (POST или PUT) для отправки запроса на сервер
    const url = '/lab8/api/courses/' + num;
    const method = num ? 'PUT' : 'POST';

    // Выполнение запроса на сервер
    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(course),
    })
    .then(function () {
        // После успешного выполнения запроса, обновить список курсов и закрыть модальное окно
        fillCourseList();
        hideModal();
    });
}

// Заполнение данных редактирования при редактировании курса
function editCourse(num, course) {
    document.getElementById('num').value = num;
    document.getElementById('name').value = course.name;
    document.getElementById('videos').value = course.videos;
    document.getElementById('price').value = course.price === 'бесплатно' ? '0' : course.price;
    delete course.createdAt;
    showModal();
}
