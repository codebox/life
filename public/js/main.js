window.onload = () => {
    "use strict";
    function uiSetup(metadata) {
        grid.style.gridTemplateColumns = `repeat(${metadata.w}, 20px)`;
        grid.style.gridTemplateRows = `repeat(${metadata.h}, 20px)`;
    }

    const grid = document.getElementById('grid');
    function render(data) {
        const locations = [];
        for (let location of Object.values(data.locations)) {
            if (!locations[location.x]) {
                locations[location.x] = [];
            }
            locations[location.x][location.y] = location;
        }
        const html = [];
        locations.forEach(row => {
            html.push(row.map(cell => `<div id="${cell.id}" style="background-color: rgba(0,255,0,${cell.food})">${cell.agent_id !== undefined ? '&#128017;' : ''}</div>`).join(''));
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


