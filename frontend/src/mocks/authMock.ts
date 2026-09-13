// src/mocks/authMock.ts

export interface AuthResponse {
  token: string;
  user: { id: number; email: string; username: string };
}

let mockUserId = 1;

export async function signup(email: string, password: string): Promise<AuthResponse> {
  // In real app, would call /auth/signup. Here we mock.
  const token = btoa(`${email}:mocktoken`);
  return {
    token,
    user: { id: mockUserId++, email, username: email.split('@')[0] },
  };
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const token = btoa(`${email}:mocktoken`);
  return {
    token,
    user: { id: mockUserId, email, username: email.split('@')[0] },
  };
}

export async function selectStarter(starterName: string): Promise<void> {
  // Mock implementation – just resolve.
  console.log('Starter selected:', starterName);
}
