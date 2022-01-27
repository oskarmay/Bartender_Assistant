document.querySelectorAll(".collapseButton").forEach(item => {
    item.addEventListener('click', event => {
        let element_id = item.getAttribute('data-bs-target').replace("#", "")
        let storage_item = JSON.parse(sessionStorage.getItem("collapse_list"))
        if (storage_item === null) {
            storage_item = []
        }
        if (storage_item.includes(element_id)) {
            const index = storage_item.indexOf(element_id);
            if (index > -1) {
                storage_item.splice(index, 1);
            }
        } else {
            storage_item.push(element_id)
        }
        sessionStorage.setItem("collapse_list", JSON.stringify(storage_item))
    })
})

function setCollapseElementShow() {
    let elements = JSON.parse(sessionStorage.getItem("collapse_list"))
    for (const element of elements) {
        document.getElementById(element).classList.add("show")
    }
}

