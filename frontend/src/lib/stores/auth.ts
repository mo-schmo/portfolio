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

import { BASE_URL } from '$lib/api';

export async function checkAuth() {
    try {
        const res = await fetch(`${BASE_URL}/auth/check`, {
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
