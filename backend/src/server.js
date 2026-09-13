require('dotenv').config();
const express = require('express');
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const prisma = new PrismaClient();
const app = express();
app.use(express.json());

// Register auth routes
const authRouter = require('./routes/auth');
const categoriesRouter = require('./routes/categories');
const tasksRouter = require('./routes/tasks');
app.use('/auth', authRouter);
app.use('/categories', categoriesRouter);
app.use('/tasks', tasksRouter);

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
