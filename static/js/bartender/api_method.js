const csrftoken = getCookie('csrftoken');

function promptRejectOrder(order_id) {
    Swal.fire({
        title: 'Odrzucanie zamówienia?',
        text: "Czy na pewno chcesz odrzucić to zamówienie?",
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: "Nie",
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Tak, anuluj!'
    }).then((result) => {
        if (result.isConfirmed) {
            rejectOrder(order_id)
        }
    })
}

function rejectOrder(order_id) {
    fetch('/bartender/api/reject_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "order_id": order_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                return res.json()
                    .then(data => {
                        console.log(data)
                        if (data.status === "order_rejected") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Odrzucono zamówienie.',
                            }).then(ref => {
                                window.location.reload()
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
                    text: 'Wystąpił błąd przy anulowaniu zamówienia.',
                })
            }
        })
}


function acceptOrder(order_id) {
    fetch('/bartender/api/accept_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "order_id": order_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                return res.json()
                    .then(data => {
                        console.log(data)
                        if (data.status === "order_accepted") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Zaakceptowano zamówienie.',
                            }).then(ref => {
                                window.location.reload()
                            })
                        } else if (data.status === "bad_order_status_for_this_action") {
                            Swal.fire({
                                icon: 'error',
                                title: 'Zły status',
                                text: 'Nie można zmienić statusu na zaakceptowano, bo zamówienie nie ma statusu utworzono.',
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
                    text: 'Wystąpił błąd przy anulowaniu zamówienia.',
                })
            }
        })
}

function inProgressOrder(order_id) {
    fetch('/bartender/api/in_progress_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "order_id": order_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                return res.json()
                    .then(data => {
                        console.log(data)
                        if (data.status === "order_in_in_progress") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Przygotowanie zamówienia.',
                            }).then(ref => {
                                window.location.reload()
                            })
                        } else if (data.status === "bad_order_status_for_this_action") {
                            Swal.fire({
                                icon: 'error',
                                title: 'Zły status',
                                text: 'Nie można zmienić statusu na w trakcie przygotowania, bo zamówienie nie ma statusu zaakceptowano.',
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
                    text: 'Wystąpił błąd przy anulowaniu zamówienia.',
                })
            }
        })
}

function completesOrder(order_id) {
    fetch('/bartender/api/complete_order', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            "order_id": order_id,
        }),
    })
        .then(response => response)
        .then(res => {
            if (res.status === 200) {
                return res.json()
                    .then(data => {
                        console.log(data)
                        if (data.status === "order_completed") {
                            Swal.fire({
                                icon: 'success',
                                title: 'Ukońćzono przygotowanie zamówienia.',
                            }).then(ref => {
                                window.location.reload()
                            })
                        } else if (data.status === "bad_order_status_for_this_action") {
                            Swal.fire({
                                icon: 'error',
                                title: 'Zły status',
                                text: 'Nie można zmienić statusu na ukończono, bo zamówienie nie ma statusu w trakcie przygotowania.',
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
                    text: 'Wystąpił błąd przy anulowaniu zamówienia.',
                })
            }
        })
}