import { useState, type SyntheticEvent } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router'
import { tokenStore } from '../../../shared/api'
import { authApi } from '../model'

export function useSignupViewModel() {
    const navigate = useNavigate()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const[confirm, setConfirm] = useState('')

    const signup = useMutation({
        mutationFn: async () => {
            //validation errors are thrown, so they show in the same error box as API errors
            if(username.trim().length < 3) throw new Error('Username must be atleast 3 characters')
            if(password.length < 8) throw new Error('Password must be at least 8 characters')
            if (password !== confirm) throw new Error("Password don't match")

            await authApi.signup(username.trim(), password)
            return authApi.login(username.trim(), password)
        },
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
        confirm,
        setConfirm,
        submit: (e: SyntheticEvent) => {
            e.preventDefault()
            signup.mutate()
        },
        isSubmitting: signup.isPending,
        error: signup.error?.message
        
        
    }
}