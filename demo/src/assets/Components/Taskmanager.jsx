
import { useState } from "react";
import useTasks from "../hooks/useTasks";

export default function Taskmanager() {
  const [title, setTitle] = useState("");
  const [warning, setWarning] = useState("");

  const {
    tasks,
    addTask,
    toggleTask,
    deleteTask,
    clearCompleted,
  } = useTasks();

  const completedCount = tasks.filter(
    (task) => task.completed
  ).length;

  const handleSubmit = (event) => {
    event.preventDefault();

    if (title.length === 0) {
      setWarning("Please enter a task title.");
      return;
    }

    if (!title.trim()) {
      setWarning("Task title cannot contain only spaces.");
      return;
    }

    const wasAdded = addTask(title);

    if (wasAdded) {
      setTitle("");
      setWarning("");
    }
  };

  return (
    <section className="panel task-panel">
      <h2>Task Manager</h2>

      <form onSubmit={handleSubmit} className="task-form">
        <input
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Enter a task..."
          aria-label="Task title"
        />

        <button type="submit">Add Task</button>
      </form>

      {warning && (
        <p className="warning" role="alert">
          {warning}
        </p>
      )}

      <div className="task-summary">
        <span>Total Tasks: {tasks.length}</span>
        <span>Completed: {completedCount}</span>
        <span>Remaining: {tasks.length - completedCount}</span>
      </div>

      {tasks.length === 0 ? (
        <p className="empty-message">
          No tasks yet. Add your first task!
        </p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className="task-item">
              <label className="task-label">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                />

                <span
                  className={
                    task.completed ? "completed" : ""
                  }
                >
                  {task.title}
                </span>
              </label>

              <button
                className="danger"
                onClick={() => deleteTask(task.id)}
                aria-label={`Delete ${task.title}`}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}

      <button
        className="secondary clear-button"
        onClick={clearCompleted}
        disabled={completedCount === 0}
      >
        Clear Completed
      </button>
    </section>
  );
}
