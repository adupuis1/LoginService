import { useState, type SyntheticEvent} from 'react'
import { useMutation  } from '@tanstack/react-query'
import { useNavigate } from 'react-router'
import { tokenStore } from '../../../shared/api'
import { authApi } from '../model'

export function useLoginViewModel() {
    const navigate = useNavigate()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const login = useMutation({
        mutationFn: () => authApi.login(username, password),
        onSuccess: (tokens) => {
            tokenStore.save(tokens)
            navigate('/account', {replace: true})
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
    }
}
