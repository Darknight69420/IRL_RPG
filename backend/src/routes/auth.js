const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const prisma = require('../..//prisma/client'); // placeholder, will be resolved via @prisma/client import

const router = express.Router();

// Helper to generate JWT
function generateToken(user) {
  const payload = { userId: user.id };
  return jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '7d' });
}

// Signup
router.post('/signup', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }
  try {
    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      return res.status(409).json({ error: 'User already exists' });
    }
    const passwordHash = await bcrypt.hash(password, 10);
    const user = await prisma.user.create({
      data: { email, passwordHash },
    });
    const token = generateToken(user);
    res.json({ token });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Login
router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }
  try {
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = generateToken(user);
    res.json({ token });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Me (protected)
router.get('/me', require('../middleware/auth').authMiddleware, async (req, res) => {
  try {
    const user = await prisma.user.findUnique({ where: { id: req.user.userId } });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    const { passwordHash, ...profile } = user;
    res.json({ user: profile });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
