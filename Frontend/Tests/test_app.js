// frontend/tests/test_app.js
const { addTask, deleteTask } = require('../app.js');

test('addTask adds a new task', () => {
    const tasks = [];
    addTask(tasks, { title: 'Test Task', description: 'Test Description', dueDate: '2023-12-31' });
    expect(tasks.length).toBe(1);
});

test('deleteTask removes a task', () => {
    const tasks = [{ id: 1, title: 'Test Task' }];
    deleteTask(tasks, 1);
    expect(tasks.length).toBe(0);
});