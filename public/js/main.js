window.onload = () => {
    "use strict";
    function uiSetup(metadata) {
        grid.style.gridTemplateColumns = `repeat(${metadata.w}, 20px)`;
        grid.style.gridTemplateRows = `repeat(${metadata.h}, 20px)`;
    }

    const grid = document.getElementById('grid');
    function render(data) {
        const html = [];
        data.locations.forEach(row => {
            html.push(row.map(cell => `<div style="background-color: rgba(0,255,0,${cell.food})">${cell.agent === null ? '' : cell.agent}</div>`).join(''));
        });
        grid.innerHTML = html.join('\n');
    }

    fetch('/metadata.json')
        .then(response => response.json())
        .then(setup)
        .catch(err => console.log(err));

    function getNewState(){
        fetch('/state.json')
            .then(response => response.json())
            .then(render)
            .catch(err => console.log(err));
    }
    function setup(metadata) {
        uiSetup(metadata);
        setInterval(getNewState, 1000);
        getNewState();
    }

};


