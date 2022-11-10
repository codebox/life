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
        ctx.fillStyle = `rgba(200,200,200,${location.food})`
        ctx.fillRect(x, y, xFactor, yFactor);
        if (location.agent) {
            const colour = location.agent.colour;
            ctx.beginPath();
            ctx.arc(x + xFactor/2, y + yFactor/2, xFactor/3, 0, 2 * Math.PI, false);
            ctx.fillStyle = colour;
            ctx.fill();
        }
    }

    function render(data) {
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        data.locations.forEach(drawLocation);
        elStatus.innerHTML = `Population ${data.population}`;
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


