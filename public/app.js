document.querySelectorAll('form').forEach(form => form.addEventListener('submit', handleForm))
const log = document.getElementById('response-container');
function handleForm(event) { event.preventDefault(); }
addEventListener('pywebviewready', main);


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
    const row = table.insertRow(-1);
    for(const value of content) {
        const cell = row.insertCell(-1);

        const element = document.createElement('p');
        element.innerText = value;
        cell.appendChild(element);
    }

    return row;
}

function removeTable() {
    document.querySelector('#results-area').innerHTML = "";
}

function createTable(data) {
    table = document.createElement('table');
    table.classList.add('data')
    removeTable();

    addRow(table, ["First Number", "Second Number", "idk", "idk", "Name", "Date"])

    for(const row of data) {
        row_arr = []
        for(const cell in row) {
            if(isNaN(Math.round(cell))) continue;
            const value = row[cell];

            row_arr[Math.round(cell)] = value;
        }

        addRow(table, row_arr);
    }

    document.querySelector('#results-area').appendChild(table);
    return table;
}

function main() {
    // Highlight column on focus
    document.querySelectorAll('#table input').forEach(input => input.addEventListener('focus', event => {
        cell = event.target.closest('td')
        column = getColumn(event.target.closest('#table'), cell);

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
    document.querySelectorAll('#table input').forEach(input => input.addEventListener('input', event => {
        document.querySelectorAll('#table input').forEach(input => {
            if(input == event.target)
                return;

            input.value = ""
        });
    }));

    // Select input on click
    document.querySelector('#table').addEventListener('click', event => {
        const cell = event.target.closest('td')
        const column = getColumn(event.target.closest('#table'), cell);

        let input = column.find(element => element.querySelector('#table input') != null);
        if(input == null) return;

        input = input.querySelector('#table input');
        if(document.activeElement != input)
            input.select();// input.focus();
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

    const col = formPackage.length;
    const val = formPackage.pop();
    if(val == null) return;
    
    const btn = document.querySelector('button[type=submit]');
    btn.disabled = true;
    
    removeTable();
    form.reset();

    pywebview.api.doSearch(val, col).then(res => {
        log.innerText = res.message + '\n';
        data = JSON.parse(res.data)["data"];
        btn.disabled = false;
        createTable(data);
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
