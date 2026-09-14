import { clear } from "console";
import { ref } from "process";

export const tokenStore = {
    get access() { return localStorage.getItem('access_token') },
    get refresh() { return localStorage.getItem('refresh_token')},
    save(t: {access_token: string; refresh_token: string}){
        localStorage.setItem('access_token', t.access_token)
        localStorage.setItem('refresh_token', t.refresh_token)
    },
    clear() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    },
}

// single-flight: if several requests get 401 at once, they share ONE refresh call
// (two refreshes with the same token would trigger the backend's reuse detection and log you out)
let refreshing: Promise<boolean> | null = null

function refreshTokens(): Promise<boolean> {
    refreshing ??= (async () => {
        const refresh_token = tokenStore.refresh
        if(!refresh_token) return false
        const res = await fetch('/api/v1/login/refresh', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({refresh_token}),
        })
        if (!res.ok) {
            tokenStore.clear
            return false
        }
        tokenStore.save(await res.json())
        return true
    })().finally(() => {
        refreshing = null
    })
    return refreshing
}