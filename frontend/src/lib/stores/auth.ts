import { writable } from 'svelte/store';

interface AuthState {
    isAuthenticated: boolean;
    isAdmin: boolean;
    loading: boolean;
}

export const auth = writable<AuthState>({
    isAuthenticated: false,
    isAdmin: false,
    loading: true
});

export async function checkAuth() {
    try {
        const res = await fetch('http://localhost:8080/api/auth/check', {
            credentials: 'include'
        });
        if (res.ok) {
            auth.set({ isAuthenticated: true, isAdmin: true, loading: false });
        } else {
            auth.set({ isAuthenticated: false, isAdmin: false, loading: false });
        }
    } catch (e) {
        auth.set({ isAuthenticated: false, isAdmin: false, loading: false });
    }
}
