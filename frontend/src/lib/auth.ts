import api from './api';

interface AuthResponse {
    access: string;
    refresh: string;
}

export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/token/', { email, password });
    return data;
};

export const registerUser = async (
    email: string,
    password: string,
    firstName = 'demo',
    lastName = 'user',
    acceptCgu = true
): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/register/', {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        accept_cgu: acceptCgu,
    });
    return data;
};

export const refreshToken = async (): Promise<string | null> => {
    const refresh = localStorage.getItem('refresh');
    if (!refresh) return null;

    try {
        const { data } = await api.post<{ access: string }>('/token/refresh/', { refresh });
        return data.access;
    } catch (error: unknown) {
        if (
            typeof error === 'object' &&
            error !== null &&
            'response' in error
        ) {
            const err = error as { response?: { data?: unknown } };
            console.warn('🔁 Token refresh failed:', err.response?.data);
        } else {
            console.warn('🔁 Token refresh error:', error);
        }
        return null;
    }
};

export const logoutUser = (): void => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
};
