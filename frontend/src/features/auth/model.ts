import { http } from '../../shared/api'

export type User = {
    id: string
    username: string
    is_superuser: boolean
    created_at: string | null
}

export type Tokens = {
    access_token: string
    refresh_token: string
}

const postJson = (body: unknown): RequestInit => ({
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify(body),
})

export const authApi = {
    // login uses FORM data (OAuth2PasswordRequestForm), not JSON
    login: (username: string, password: string) => 
        http<Tokens>(
            '/api/v1/login/access-token',
            {method: 'POST', body: new URLSearchParams({ username, password }) },
            false,
        ),

    signup: (username: string, password: string) =>
        http<User>('/api/v1/users/signup', postJson({ username, password }), false),

    me: () => http<User>('/api/v1/users/self'),

    logout: (refresh_token: string) =>
        http<{message: string}>('/api/v1/logout', postJson({ refresh_token }), false)
}