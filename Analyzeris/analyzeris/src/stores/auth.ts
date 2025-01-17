import { defineStore } from 'pinia';
import axios from 'axios';
import { readonly, ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // saugiai isgauti ir issaugoti localstorage reiksmes arba nustatyti null
  const parseLocalStorage = (key: string): string | null => {
    const item = localStorage.getItem(key);
    // grazinam null jei reiksmes nera
    if (!item) return null;
    try {
      return JSON.parse(item);
    } catch (e) {
      console.warn(`Failed to parse localStorage key "${key}":`, e);
      return null; // grazinam null jei issaugojimas nepavyko
    }
  };

  const username = ref<string | null>(parseLocalStorage('username'));
  const authToken = ref<string | null>(parseLocalStorage('access_token'));
  const refreshToken = ref<string | null>(parseLocalStorage('refresh_token'));
  const isAuthenticated = ref<boolean>(!!authToken.value);

  // Actions
  async function login(username: string, password: string): Promise<boolean> {
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        username,
        password,
      });

      localStorage.setItem('access_token', JSON.stringify(response.data.access_token));
      localStorage.setItem('refresh_token', JSON.stringify(response.data.refresh_token));
      localStorage.setItem('username', JSON.stringify(username));

      authToken.value = response.data.access;
      refreshToken.value = response.data.refresh;
      isAuthenticated.value = true;
      authToken.value = JSON.parse(localStorage.getItem('access_token')!);

      return true;
    } catch (error) {
      console.error('Login error:', error);
      throw error; 
    }
  }

  async function logout(): Promise<void> {
    authToken.value = null;
    refreshToken.value = null;
    isAuthenticated.value = false;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
  }

  return { login, logout, authToken: readonly(authToken), refreshToken: readonly(refreshToken), 
    isAuthenticated: readonly(isAuthenticated), username: readonly(username), };
});
