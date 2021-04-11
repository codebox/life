window.onload = () => {
    "use strict";
    function uiSetup(metadata) {
        grid.style.gridTemplateColumns = `repeat(${metadata.w}, 20px)`;
        grid.style.gridTemplateRows = `repeat(${metadata.h}, 20px)`;
    }

    const grid = document.getElementById('grid');
    function render(data) {
        const html = [];
        data.forEach(row => {
            html.push(row.map(cell => `<div>${cell}</div>`).join(''));
        });
        grid.innerHTML = html.join('\n');
    }

    fetch('/metadata.json')
        .then(response => response.json())
        .then(setup)
        .catch(err => console.log(err));

    function setup(metadata) {
        uiSetup(metadata);
        setInterval(() => {
            "use strict";
            fetch('/state.json')
                .then(response => response.json())
                .then(render)
                .catch(err => console.log(err));
        }, 1000);
    }

};


