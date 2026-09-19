import { useState, type SyntheticEvent} from 'react'
import { useMutation  } from '@tanstack/react-query'
import { useSearchParams } from 'react-router'
import { tokenStore } from '../../../shared/api'
import { authApi } from '../model'


export function safeNext(next: string | null){
    return next?.startsWith('/') && !next.startsWith('//') ? next : '/auth/account'
}

export function useLoginViewModel() {
    const [params] = useSearchParams()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const login = useMutation({
        mutationFn: () => authApi.login(username, password),
        onSuccess: (tokens) => {
            tokenStore.save(tokens)
            window.location.assign(safeNext(params.get('next')))
        },
    })

    return {
        username,
        setUsername,
        password,
        setPassword,
        submit: (e: SyntheticEvent) => {
            e.preventDefault()
            login.mutate()
        },
        isSubmitting: login.isPending,
        error: login.error?.message,
        signupHref: `/signup?${params}`, // keep ?next = when switching to signup
    }
}
