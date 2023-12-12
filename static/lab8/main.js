function fillCourseList() {
    fetch('/lab8/api/courses/')
        .then(function (data) {
            return data.json();
        })
        .then(function (courses) {
            let tbody = document.getElementById('course-list');
            tbody.innerHTML = '';
            for (let i = 0; i < courses.length; i++) {
                let tr = document.createElement('tr');

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

                tr.append(tdName);
                tr.append(tdVideos);
                tr.append(tdPrice);
                tr.append(tdActions);
                tr.append(tdDATA);
                tbody.append(tr);
            }
        });
}

function deleteCourse(num) {
    if (!confirm('Вы точно хотите удалить курс?')) {
        return;
    }

    fetch('/lab8/api/courses/' + num, { method: 'DELETE' })
        .then(function () {
            fillCourseList();
        })
        .catch(function (error) {
            console.error('Ошибка при удалении курса:', error);
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addCourse() {
    const course = {};
    delete course.createdAt;
    document.getElementById('num').value = '';
    document.getElementById('name').value = '';
    document.getElementById('videos').value = '';
    document.getElementById('price').value = '';
    showModal();
}

function sendCourse() {
    const num = document.getElementById('num').value;
    const name = document.getElementById('name').value;
    const videos = document.getElementById('videos').value;
    const price = document.getElementById('price').value;

    // Check if price is 0 and set it to 'бесплатно'
    const normalizedPrice = price === '0' ? 'бесплатно' : price;

    if (!name || !videos) {
        alert('Заполните все поля!');
        return;
    }

    const course = {
        name: name,
        videos: videos,
        price: normalizedPrice,
    };

    const url = '/lab8/api/courses/' + num;
    const method = num ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(course),
    })
    .then(function () {
        fillCourseList();
        hideModal();
    });
}

function editCourse(num, course) {
    document.getElementById('num').value = num;
    document.getElementById('name').value = course.name;
    document.getElementById('videos').value = course.videos;
    document.getElementById('price').value = course.price === 'бесплатно' ? '0' : course.price;
    delete course.createdAt;
    showModal();
}
