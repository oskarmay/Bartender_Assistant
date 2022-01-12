const csrftoken = getCookie('csrftoken');

function PromptCancelOrder(ordered_id) {
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
            CancelOrder(ordered_id)
        }
    })
}

function createOrder(order_id, is_drink) {
    fetch('/customer/api/create_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "order_id": order_id,
            "is_drink": is_drink,
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
                                    'Poczekaj na swoje zamówienia lub anuluj jedno ze statusem utworzono.',
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

function CancelOrder(ordered_id) {
    fetch('/customer/api/cancel_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "ordered_id": ordered_id,
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
                            }).then(ref => {
                                window.location.reload()
                            })
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