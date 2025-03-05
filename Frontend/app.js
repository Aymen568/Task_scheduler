const baseUrl = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');
    const graphDiv = document.getElementById('graph');

    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const topic = document.getElementById('topic').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const timeStart = document.getElementById('time-start').value;
        const timeEnd = document.getElementById('time-end').value;
        const dependencies = document.getElementById('dependencies').value
            .split(',')
            .map(id => parseInt(id.trim()))
            .filter(id => !isNaN(id));

        const response = await fetch(`${baseUrl}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, title, description, timeStart, timeEnd, dependencies })
        });
        const task = await response.json();
        fetchTasks();
    });

    async function fetchTasks() {
        const response = await fetch(`${baseUrl}/tasks`);
        const tasks = await response.json();
        renderTasks(tasks);
        renderGraph(tasks);
    }

    function renderTasks(tasks) {
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const taskItem = document.createElement('li');
            taskItem.innerHTML = `
                <div>
                    <strong>${task.topic}: ${task.title}</strong>
                    <p>${task.description}</p>
                    <small>Start: ${task.timeStart}, End: ${task.timeEnd}</small>
                    <small>Dependencies: ${task.dependencies.join(', ')}</small>
                </div>
                <button onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(taskItem);
        });
    }

    function renderGraph(tasks) {
        const nodes = tasks.map(task => ({ id: task.id, label: `${task.topic}: ${task.title}` }));
        const edges = tasks.flatMap(task =>
            task.dependencies.map(depId => ({ from: depId, to: task.id }))
        );

        const data = {
            nodes: nodes,
            edges: edges
        };

        const options = {
            layout: {
                hierarchical: {
                    enabled: true,
                    direction: 'LR', // Left to Right
                    sortMethod: 'directed'
                }
            },
            edges: {
                arrows: 'to'
            }
        };

        // Clear previous graph
        graphDiv.innerHTML = '';
        const network = new vis.Network(graphDiv, data, options);
    }

    window.deleteTask = async (taskId) => {
        await fetch(`${baseUrl}/tasks/${taskId}`, { method: 'DELETE' });
        fetchTasks();
    };

    fetchTasks();
});