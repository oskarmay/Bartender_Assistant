const csrftoken = getCookie('csrftoken');

function orderDrink(drink_id) {
    fetch('api/order_drink', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "drink_id": drink_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                console.log(res.body)
                return res.json()
                    .then(data => {
                        if (data.status === "order_created") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Złożono zamówienie',
                            })
                        } else if (data.status === "too_many_orders") {
                            Swal.fire({
                                icon: 'warning',
                                title: 'Ktoś chce szybko skończyć wieczór',
                                text: 'Mamy limit aktualnie obsługiwanych zamówień (4 na klienta). ' +
                                    'Poczekaj na swoje zamówienia lub anuluj jedno ze statusem utorzono.',
                            })
                        }

                    })

            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Coś poszło nie tak...',
                    text: 'Wystąpił błąd przy składaniu zamówienia',
                })
            }
            console.log(res.status)
            // temp = res.json()
            // console.log(temp)
            // {
            // return response.json() //Convert response to JSON
            // }
        })
    // .then(data => {
    //     console.log(data)
    // })
}

//
// const csrftoken = getCookie('csrftoken');
//
// function orderDrink(drink_id) {
//     fetch('api/order_drink', {
//         method: 'POST',
//         mode: 'same-origin',
//         headers: {
//             'Accept': 'application/json, text/plain, */*',
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         body: JSON.stringify({
//             "drink_id": drink_id,
//         }),
//     })
//         .then(response => response)
//         .then(res => {
//             if (res.status === 200) {
//                 console.log(res.body)
//                 Swal.fire({
//                     icon: 'success',
//                     title: 'Złożono zamówienie',
//                 })
//             } else {
//                 Swal.fire({
//                     icon: 'error',
//                     title: 'Coś poszło nie tak...',
//                     text: 'Wystąpił błąd przy składaniu zamówienia',
//                 })
//             }
//         })
// }