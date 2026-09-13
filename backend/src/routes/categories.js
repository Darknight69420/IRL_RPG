const express = require('express');
const router = express.Router();

// Hardcoded categories list (could be seeded via script)
const categories = [
  { id: 1, name: 'Fitness' },
  { id: 2, name: 'Intellect' },
  { id: 3, name: 'Vitality' },
];

// GET /categories – return list of categories
router.get('/', (req, res) => {
  res.json({ categories });
});

module.exports = router;
