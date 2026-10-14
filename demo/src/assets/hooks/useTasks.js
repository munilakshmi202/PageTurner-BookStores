
import { useState } from "react";

function createTaskId() {
  if (typeof crypto !== "undefined" &&
      typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export default function useTasks() {
  const [tasks, setTasks] = useState([]);

  const addTask = (title) => {
    if (typeof title !== "string" || !title.trim()) {
      return false;
    }

    const newTask = {
      id: createTaskId(),
      title: title.trim(),
      completed: false,
    };

    setTasks((previousTasks) => [
      ...previousTasks,
      newTask,
    ]);

    return true;
  };

  const toggleTask = (taskId) => {
    setTasks((previousTasks) =>
      previousTasks.map((task) =>
        task.id === taskId
          ? { ...task, completed: !task.completed }
          : task
      )
    );
  };

  const deleteTask = (taskId) => {
    setTasks((previousTasks) =>
      previousTasks.filter((task) => task.id !== taskId)
    );
  };

  const clearCompleted = () => {
    setTasks((previousTasks) =>
      previousTasks.filter((task) => !task.completed)
    );
  };

  return {
    tasks,
    addTask,
    toggleTask,
    deleteTask,
    clearCompleted,
  };
}
