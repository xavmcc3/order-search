document.querySelectorAll('form').forEach(form => form.addEventListener('submit', handleForm))
const log = document.getElementById('response-container');
function handleForm(event) { event.preventDefault(); }
addEventListener('pywebviewready', main);
let observer = new IntersectionObserver(
    (entries) => entries.forEach(e => {
        e.target.toggleAttribute('stuck', e.intersectionRatio < 1)
    }),
    {
        rootMargin: "0px",
        threshold: 1.0,
        root: null
    }
);

function addToLog(msg) {
    const parent = document.querySelector('#cmd');
    const text = document.createElement('p');
    text.innerHTML = msg;

    parent.insertAdjacentElement('afterbegin', text);
    return text.innerText;
}

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
    try {
        observer.unobserve(document.querySelector('#results-area table:first-child'));
    } catch (error) { }
    
    table = document.createElement('table');
    table.classList.add('data');
    removeTable();

    const COLUMN_NAMES = ["Delivery", "CO", "Quantity", "Logos", "Operator", "Date"];
    addRow(table, COLUMN_NAMES);

    for(const row of data) {
        row_arr = []
        for(const key of COLUMN_NAMES) {
            const value = row[key];
            row_arr[COLUMN_NAMES.indexOf(key)] = value;
        }

        addRow(table, row_arr);
    }

    document.querySelector('#results-area').appendChild(table);
    observer.observe(table.querySelector('tr'));
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

    // Use the folder picker button
    document.querySelector('#folder-picker').addEventListener('click', async () => {
        pywebview.api.setFolder().then(res => {
            if(res.path != null)
                document.querySelector('#folder-picker').querySelector('.string').innerText = res.path;
            log.innerText = res.message + '\n';
        }).catch(err => {
            log.innerText = err.message + '\n';
        })
    });

    // Use the file picker button
    document.querySelector('#file-picker').addEventListener('click', async () => {
        pywebview.api.setFile().then(async res => {
            if(res.path != null)
                document.querySelector('#file-picker').querySelector('.string').innerText = res.path;
            log.innerText = res.message + '\n';

            const date = await pywebview.api.getLastModified();
            document.querySelector('#last-edit').innerText = date.date;
        }).catch(err => {
            log.innerText = err.message + '\n';
        })
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
        document.querySelector('#file-picker').querySelector('.string').innerText = res.path;
        log.innerText = res.message + '\n';
        data = JSON.parse(res.data)["data"];
        btn.disabled = false;
        createTable(data);
    }).catch(err => {
        log.innerText = err.message + '\n';
    })
}
async function updateIndex() {
    const btn = document.querySelector('button[type=submit]');
    document.querySelector('#full').classList.add('active');
    document.querySelector('#update').disabled = true;
    btn.disabled = true;

    pywebview.api.updateIndex().then(async res => {
        document.querySelector('#update').disabled = false;
        document.querySelector('#cmd').innerHTML = ""
        log.innerText = res.message + '\n';
        btn.disabled = false;
        removeTable();

        const date = await pywebview.api.getLastModified();
        document.querySelector('#full').classList.remove('active');
        document.querySelector('#last-edit').innerText = date.date;
    });
}

async function openErrLog() {
    await pywebview.api.openErrLog();
}

async function openCsv() {
    await pywebview.api.openCsv();
}

function initialize() {
    pywebview.api.init().then(res => {
        document.querySelector('#folder-picker').querySelector('.string').innerText = res.path;
        document.querySelector('#file-picker').querySelector('.string').innerText = res.csv;
        showResponse(res);
    })

    pywebview.api.getLastModified().then(res => {
        document.querySelector('#last-edit').innerText = res.date;
    })
}

function destroy() {
    pywebview.api.destroy().then()
}
