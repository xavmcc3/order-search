document.querySelectorAll('form').forEach(form => form.addEventListener('submit', handleForm))
const log = document.getElementById('response-container');
function handleForm(event) { event.preventDefault(); }
addEventListener('pywebviewready', main);
addEventListener("wheel", () => {
    if(document.activeElement.type === "number"){
        // document.activeElement.blur();
    }
});


function getColumn(table, cell) {
    if(cell == null) return [];
    const parent = cell.parentNode;
    const index = Array.prototype.indexOf.call(parent.children, cell);
    
    const rows = table.querySelectorAll('tr');
    const column = []
    for(row of rows) {
        const element = row.children[index];
        column.push(element);
    }

    return column;
}

function resetTable(table) {
    while(table.children[0].children.length > 2) {
        table.children[0].removeChild(table.children[0].lastChild);
    }
}

function addRow(table, content) {
    const parent = table.getElementsByTagName('tbody')[0];
    const row = parent.insertRow(-1);
    for(const value of content) {
        const cell = row.insertCell(0);

        const element = document.createElement('p');
        element.innerText = value;
        cell.appendChild(element);
    }

    return row;
}

function main() {
    // Highlight column on focus
    document.querySelectorAll('table input').forEach(input => input.addEventListener('focus', event => {
        cell = event.target.closest('td')
        column = getColumn(event.target.closest('table'), cell);

        document.querySelectorAll('td.selected').forEach(td => {
            if(td == cell)
                return;
            td.classList.remove('selected')
        });

        column.forEach(td => {
            if(td == null) return;
            td.classList.add('selected')
        });
    }));

    // Remove other inputs on type
    document.querySelectorAll('table input').forEach(input => input.addEventListener('input', event => {
        document.querySelectorAll('table input').forEach(input => {
            if(input == event.target)
                return;

            input.value = ""
        });
    }));

    // Select input on click
    document.querySelector('table').addEventListener('click', event => {
        const cell = event.target.closest('td')
        const column = getColumn(event.target.closest('table'), cell);

        let input = column.find(element => element.querySelector('table input') != null);
        if(input == null) return;

        input = input.querySelector('table input');
        if(document.activeElement != input)
            input.focus();
    });

    initialize();
}


function showResponse(res) {
    log.innerText += res.message + '\n';
}

function doSearch(form) {
    const formPackage = [];
    form.querySelectorAll('input').forEach(input => {
        if(input.value == null || input.value == "") return;
        cell = input.closest('td');
        if(cell == null) return;

        const index = Array.prototype.indexOf.call(cell.parentNode.children, cell);
        formPackage[index] = input.value;
    });

    pywebview.api.doSearch(formPackage).then(res => {
        log.innerText = res.data + '\n';
    }).catch(err => {
        log.innerText = err.message + '\n';
    })
}

function initialize() {
    pywebview.api.init().then(showResponse)
}

function destroy() {
    pywebview.api.destroy().then()
}
