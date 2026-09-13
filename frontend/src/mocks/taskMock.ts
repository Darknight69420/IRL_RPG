// src/mocks/taskMock.ts

export type Difficulty = "Easy" | "Medium" | "Hard";

export interface Task {
  id: number;
  categoryId: number;
  title: string;
  description: string;
  difficulty: Difficulty;
  completed: boolean;
}

let nextId = 1;
let tasks: Task[] = [];

/** Retrieve tasks for a given category */
export async function getTasksByCategory(categoryId: number): Promise<Task[]> {
  return new Promise((resolve) =>
    setTimeout(() => resolve(tasks.filter((t) => t.categoryId === categoryId)), 100),
  );
}

/** Create a new task */
export async function createTask(params: {
  categoryId: number;
  title: string;
  description: string;
  difficulty: Difficulty;
}): Promise<Task> {
  const newTask: Task = {
    id: nextId++,
    categoryId: params.categoryId,
    title: params.title,
    description: params.description,
    difficulty: params.difficulty,
    completed: false,
  };
  tasks.push(newTask);
  return new Promise((resolve) => setTimeout(() => resolve(newTask), 100));
}

/** Update an existing task */
export async function updateTask(updated: Task): Promise<Task> {
  const idx = tasks.findIndex((t) => t.id === updated.id);
  if (idx !== -1) tasks[idx] = { ...tasks[idx], ...updated };
  return new Promise((resolve) => setTimeout(() => resolve(tasks[idx]), 100));
}

/** Delete a task */
export async function deleteTask(taskId: number): Promise<void> {
  tasks = tasks.filter((t) => t.id !== taskId);
  return new Promise((resolve) => setTimeout(() => resolve(), 100));
}

/** Mark a task as complete */
export async function completeTask(taskId: number): Promise<Task | undefined> {
  const task = tasks.find((t) => t.id === taskId);
  if (task) task.completed = true;
  return new Promise((resolve) => setTimeout(() => resolve(task), 100));
}
