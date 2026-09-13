const express = require('express');
const router = express.Router();
const { authMiddleware } = require('../middleware/auth');
const prisma = require('../../prisma/client'); // Assuming client export

// POST /tasks – create a task
router.post('/', authMiddleware, async (req, res) => {
  const { title, description, categoryId, difficulty } = req.body;
  if (!title || !categoryId || difficulty == null) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  try {
    const task = await prisma.task.create({
      data: {
        title,
        description,
        difficulty,
        categoryId,
        userId: req.user.userId,
      },
    });
    res.status(201).json(task);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /tasks – list user's tasks, optional filter by categoryId
router.get('/', authMiddleware, async (req, res) => {
  const { categoryId } = req.query;
  const where = { userId: req.user.userId };
  if (categoryId) where.categoryId = Number(categoryId);
  try {
    const tasks = await prisma.task.findMany({ where });
    res.json(tasks);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PATCH /tasks/:id – update task fields
router.patch('/:id', authMiddleware, async (req, res) => {
  const { id } = req.params;
  const { title, description, difficulty } = req.body;
  try {
    const existing = await prisma.task.findUnique({ where: { id: Number(id) } });
    if (!existing || existing.userId !== req.user.userId) {
      return res.status(404).json({ error: 'Task not found' });
    }
    const updated = await prisma.task.update({
      where: { id: Number(id) },
      data: { title, description, difficulty },
    });
    res.json(updated);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /tasks/:id – delete task
router.delete('/:id', authMiddleware, async (req, res) => {
  const { id } = req.params;
  try {
    const existing = await prisma.task.findUnique({ where: { id: Number(id) } });
    if (!existing || existing.userId !== req.user.userId) {
      return res.status(404).json({ error: 'Task not found' });
    }
    await prisma.task.delete({ where: { id: Number(id) } });
    res.json({});
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /tasks/:id/complete – mark as completed
router.post('/:id/complete', authMiddleware, async (req, res) => {
  const { id } = req.params;
  try {
    const task = await prisma.task.findUnique({ where: { id: Number(id) } });
    if (!task || task.userId !== req.user.userId) {
      return res.status(404).json({ error: 'Task not found' });
    }
    if (task.completedAt) {
      return res.status(400).json({ error: 'Task already completed' });
    }
    const updated = await prisma.task.update({
      where: { id: Number(id) },
      data: { completedAt: new Date() },
    });
    res.json(updated);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
