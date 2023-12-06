function get_price() {
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;
    const drink = document.querySelector('[name=drink]:checked').value;

    const obj = {
        "method": "get-price",
        "params": {
            drink: drink,
            milk: milk,
            sugar: sugar
        }
    };

    fetch('/lab7/api', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(obj)
        })
        .then(function(resp) {
            return resp.json();
        })
        .then(function(data){
            document.querySelector('#price').innerHTML = `Цена напитка: ${data.result} руб`;
            document.querySelector('#pay').style.display = '';
            document.querySelector('#refund').style.display = '';
        })
}

function pay() {
    const cardNum = document.querySelector('[name=card]').value;
    const cardName = document.querySelector('[name=name]').value;
    const cvv = document.querySelector('[name=cvv]').value;
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;
    const drink = document.querySelector('[name=drink]:checked').value;

    const obj = {
        "method": "pay",
        "params": {
            card_num: cardNum,
            card_name: cardName,
            cvv: cvv,
            drink: drink,
            milk: milk,
            sugar: sugar
        }
    };

    fetch('/lab7/api', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(obj)
        })
        .then(function(resp) {
            return resp.json();
        })
        .then(function(data){
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.result);
            }
        })
}


function refund() {
    const cardNum = document.querySelector('[name=card]').value;
    const cvv = document.querySelector('[name=cvv]').value;
    const drink = document.querySelector('[name=drink]:checked').value;
    const milk = document.querySelector('[name=milk]').checked;
    const sugar = document.querySelector('[name=sugar]').checked;

    const obj = {
        "method": "refund",
        "params": {
            card_num: cardNum,
            cvv: cvv,
            drink: drink,
            milk: milk,
            sugar: sugar
        }
    };

    fetch('/lab7/refund', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(obj)
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(data){
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.result);
        }
    })
}