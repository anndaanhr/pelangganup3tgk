import { api } from './api';

export const login = async (username: string, password: string): Promise<{ access_token: string; token_type: string }> => {
    // OAuth2PasswordRequestForm expects form-data, not JSON
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
