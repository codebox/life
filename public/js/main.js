window.onload = () => {
    "use strict";

    const elStatus = document.getElementById('status'),
        canvas = document.getElementById('grid'),
        ctx = canvas.getContext('2d'),
        canvasWidth = canvas.width,
        canvasHeight = canvas.height;

    ctx.font = '8px sans-serif';

    let gridWidth, gridHeight, xFactor, yFactor, prevAge = 0;
    function uiSetup(metadata) {
        gridWidth = metadata.w;
        gridHeight = metadata.h;
        xFactor = canvasWidth / gridWidth;
        yFactor = canvasHeight / gridHeight;
    }

    function drawLocation(location, showAgentIds) {
        const x = location.coords.x * xFactor,
            y = location.coords.y * yFactor;
        ctx.fillStyle = `rgba(200,200,200,${location.food})`
        ctx.fillRect(x, y, xFactor, yFactor);
        if (location.agent) {
            const colour = location.agent.colour;
            if (location.agent.type === 'herbivore') {
                ctx.beginPath();
                ctx.arc(x + xFactor / 2, y + yFactor / 2, xFactor / 3, 0, 2 * Math.PI, false);
                ctx.fillStyle = colour;
                ctx.fill();
            } else if (location.agent.type === 'carnivore') {
                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x + xFactor, y + yFactor);
                ctx.moveTo(x, y + yFactor);
                ctx.lineTo(x + xFactor, y);
                ctx.strokeStyle = colour;
                ctx.stroke();
            }
            if (showAgentIds) {
                ctx.fillText(location.agent.id, x + xFactor / 2 + 5, y + yFactor / 2 - 5);
            }
        }
    }

    const graph = (() => {
        const canvas = document.getElementById('graph'),
            ctx = canvas.getContext('2d'),
            canvasWidth = canvas.width,
            canvasHeight = canvas.height,
            data = {
                'carnivore': {
                    'color': 'red',
                    'values': []
                },
                'herbivore': {
                    'color': 'green',
                    'values': []
                }
            };
        let maxValue = 0;
        return {
            reset(){
                [...Object.keys(data)].forEach(speciesName => data[speciesName].values = []);
            },
            update(values) {
                [...Object.keys(values)].forEach(speciesName => {
                    const value = values[speciesName];
                    maxValue = Math.max(value, maxValue);
                    data[speciesName].values.push(value);
                });
                ctx.clearRect(0, 0, canvasWidth, canvasHeight);
                [...Object.keys(values)].forEach(speciesName => {
                    ctx.beginPath();
                    ctx.moveTo(0, canvasHeight);
                    const values = data[speciesName].values;
                    let x, y;
                    values.forEach((value, i) => {
                        x = i;
                        y = canvasHeight - canvasHeight * value / maxValue;
                        ctx.lineTo(x, y);
                    });
                    ctx.strokeStyle = data[speciesName].color;
                    ctx.fillText(data[speciesName].values[x], x, y);
                    ctx.stroke();
                });
            }
        };
    })();

    function render(data) {
        if (data.age < prevAge) {
            graph.reset();
        }
        prevAge = data.age;
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        const agentCount = data.locations.filter(l => l.agent).length;
        data.locations.forEach(location => drawLocation(location, agentCount < 100));
        graph.update(data.population);
        const population = [...Object.values(data.population)].reduce((a,b) => a + b, 0);
        elStatus.innerHTML = `Population ${population}<br>Age ${Math.round(data.age/1000)}k`;
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


