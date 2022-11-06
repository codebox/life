window.onload = () => {
    "use strict";

    const elStatus = document.getElementById('status'),
        canvas = document.getElementById('grid'),
        ctx = canvas.getContext('2d'),
        canvasWidth = canvas.width,
        canvasHeight = canvas.height;

    let gridWidth, gridHeight, xFactor, yFactor;
    function uiSetup(metadata) {
        gridWidth = metadata.w;
        gridHeight = metadata.h;
        xFactor = canvasWidth / gridWidth;
        yFactor = canvasHeight / gridHeight;
    }

    function drawLocation(location) {
        const x = location.x * xFactor,
            y = location.y * yFactor;
        ctx.fillStyle = `rgba(0,255,0,${location.food})`
        ctx.fillRect(x, y, xFactor, yFactor);
        if (location.agent_id) {
            ctx.beginPath();
            ctx.arc(x + xFactor/2, y + yFactor/2, xFactor/4, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'black';
            ctx.fill();
        }
    }

    function render(data) {
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        for (let location of Object.values(data.locations)) {
            drawLocation(location);
        }
        elStatus.innerHTML = `Generation ${data.generation}`;
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


