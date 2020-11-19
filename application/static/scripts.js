const dropdown = document.getElementById('symbols');
const chart = document.getElementById('chart');

dropdown.addEventListener("change", update_symbol);

function update_symbol(){

    const idx = dropdown.selectedIndex;
    if(idx == 0){
        return
    };
    
    const options = dropdown.selectedOptions;
    let symbols = [];
    for(let i = 0; i < options.length; i++){
        symbols.push(options[i].text);
    }
    fetch(
        `http://localhost:5000/symbol/${symbols.join(',')}`, {
            method : 'POST',
            headers : {
                'Content-Type' : 'text/plain'
            },
            body : symbols.innerText
        }
    ).then(
        () => {
            fetch(
                'http://localhost:5000/chart'
            ).then(
                response => response.text()
            ).then(
                data => {
                    chart.innerHTML = `${data}`
                }
            )
        }
    );

}