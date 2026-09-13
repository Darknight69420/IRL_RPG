// src/screens/Home.tsx
import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { getCategories, Category } from '../mocks/categoryMock';
import { getTasksByCategory, createTask, updateTask, deleteTask, completeTask, Task } from '../mocks/taskMock';

// Simple modal component for mobile bottom sheet
const TaskModal: React.FC<{
  category: Category | null;
  onClose: () => void;
}> = ({ category, onClose }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newDiff, setNewDiff] = useState<'Easy' | 'Medium' | 'Hard'>('Easy');

  useEffect(() => {
    if (category) {
      getTasksByCategory(category.id).then(setTasks);
    }
  }, [category]);

  const refresh = () => {
    if (category) getTasksByCategory(category.id).then(setTasks);
  };

  const handleCreate = async () => {
    if (!category) return;
    await createTask({
      categoryId: category.id,
      title: newTitle,
      description: newDesc,
      difficulty: newDiff,
    });
    setNewTitle('');
    setNewDesc('');
    refresh();
  };

  const handleUpdate = async (task: Task) => {
    await updateTask(task);
    refresh();
  };

  const handleDelete = async (id: number) => {
    await deleteTask(id);
    refresh();
  };

  const handleComplete = async (id: number) => {
    await completeTask(id);
    refresh();
  };

  if (!category) return null;

  return (
    <div className="fixed inset-0 flex items-end justify-center bg-black bg-opacity-50" onClick={onClose}>
      <div className="bg-white w-full max-w-md rounded-t-lg p-4" onClick={e => e.stopPropagation()} style={{ height: '70vh' }}>
        <h2 className="text-xl font-semibold mb-2">{category.name} Tasks</h2>
        {/* Task List */}
        <ul className="space-y-2 overflow-auto flex-1 mb-4">
          {tasks.map(task => (
            <li key={task.id} className="flex items-center justify-between p-2 border rounded">
              <div className="flex-1">{task.completed ? <s>{task.title}</s> : task.title}</div>
              <div className="flex space-x-1">
                <button className="text-sm text-blue-600" onClick={() => handleComplete(task.id)}>{task.completed ? '✓' : 'Complete'}</button>
                <button className="text-sm text-gray-600" onClick={() => handleDelete(task.id)}>Del</button>
              </div>
            </li>
          ))}
        </ul>
        {/* New Task Form */}
        <div className="border-t pt-2">
          <h3 className="text-lg font-medium mb-1">New Task</h3>
          <input className="w-full mb-1 p-1 border rounded" placeholder="Title" value={newTitle} onChange={e => setNewTitle(e.target.value)} />
          <textarea className="w-full mb-1 p-1 border rounded" placeholder="Description" value={newDesc} onChange={e => setNewDesc(e.target.value)} />
          <select className="w-full mb-2 p-1 border rounded" value={newDiff} onChange={e => setNewDiff(e.target.value as any)}>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
          <button className="w-full bg-blue-500 text-white py-1 rounded" onClick={handleCreate}>Add Task</button>
        </div>
        <button className="mt-2 w-full text-center text-gray-500" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

const Home: React.FC = () => {
  const { user } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCatId, setSelectedCatId] = useState<number | null>(null);
  const [openModalCat, setOpenModalCat] = useState<Category | null>(null);

  useEffect(() => {
    getCategories().then(setCategories);
  }, []);

  const handleNpcClick = (cat: Category) => {
    setSelectedCatId(cat.id);
    setOpenModalCat(cat);
  };

  return (
    <div className="relative min-h-screen bg-gray-100 p-4" style={{ maxWidth: '375px', margin: '0 auto' }}>
      <h1 className="text-xl font-bold mb-4">Welcome, {user?.username || 'Guest'}!</h1>
      {/* Hub grid */}
      <div className="grid grid-cols-3 gap-2">
        {categories.map(cat => (
          <div
            key={cat.id}
            className="relative flex items-center justify-center h-20 bg-gray-200 cursor-pointer"
            onClick={() => handleNpcClick(cat)}
          >
            {/* Avatar if selected */}
            {selectedCatId === cat.id && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-8 h-8 bg-red-500 rounded-full" title="Avatar" />
              </div>
            )}
            <span className="text-sm font-medium" title={cat.name}>{cat.name}</span>
          </div>
        ))}
        {/* Grass patch placeholder */}
        <div className="flex items-center justify-center h-20 bg-green-300">
          <span className="text-sm font-medium">Grass Patch</span>
        </div>
      </div>

      {/* Task Modal */}
      {openModalCat && (
        <TaskModal category={openModalCat} onClose={() => setOpenModalCat(null)} />
      )}
    </div>
  );
};

export default Home;
