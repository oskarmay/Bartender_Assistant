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
        })
}
temp = " (\" + ordered_drink_name + \")\""
function PromptCancelOrderedDrink(ordered_drink_id) {
    Swal.fire({
        title: 'Anulowanie zamówienia?',
        text: "Czy na pewno chcesz anulować zamówienie?",
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: "Nie",
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Tak, anuluj!'
    }).then((result) => {
        if (result.isConfirmed) {
            CancelOrderedDrink(ordered_drink_id)
        }
    })
}

function CancelOrderedDrink(ordered_drink_id) {
    fetch('api/cancel_order_drink', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "ordered_drink_id": ordered_drink_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                return res.json()
                    .then(data => {
                        if (data.status === "order_canceled") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Anulowano zamówienie',
                            }).then(ref => {window.location.reload()})
                        } else if (data.status === "too_late_to_cancel_order") {
                            Swal.fire({
                                icon: 'warning',
                                title: 'Zamówienie nie może być anulowane',
                                text: 'Wygląda na to że barman przyjął już to zamówienie.',
                            })
                        } else if (data.status === "does_not_exist") {
                            Swal.fire({
                                icon: 'error',
                                title: 'Nie możemy znaleźć tego zamówienia',
                                text: 'Wystąpił nieoczekiwany problem ze znalezieniem tego zamówienia. Przepraszamy za kłopoty.',
                            })
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Coś poszło nie tak pytanie co?',
                                text: 'Nie jesteśmy w stanie odszyfrować tego błędu.',
                            })
                        }

                    })

            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Coś poszło nie tak...',
                    text: 'Wystąpił błąd przy anulowaniu zamówienia',
                })
            }
        })
}