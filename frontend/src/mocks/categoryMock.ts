// src/mocks/categoryMock.ts

export interface Category {
  id: number;
  name: string;
  // optional color or placeholder for future assets
  color?: string;
}

// In‑memory mock data
let categories: Category[] = [
  { id: 1, name: "Fitness Gym", color: "bg-blue-200" },
  { id: 2, name: "Study Library", color: "bg-green-200" },
  { id: 3, name: "Cooking School", color: "bg-yellow-200" },
];

/** Retrieve all categories */
export async function getCategories(): Promise<Category[]> {
  // Simulate async delay
  return new Promise((resolve) => setTimeout(() => resolve([...categories]), 100));
}

/** Find a category by id */
export async function getCategoryById(id: number): Promise<Category | undefined> {
  return categories.find((c) => c.id === id);
}
