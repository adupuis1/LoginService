import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { tokenStore } from "../../../shared/api";
import { authApi } from "../model";

export function useAccountViewModel() {
    const navigate = useNavigate()
    const hasToken = tokenStore.access !== null

    const me = useQuery({
        queryKey: ['me'],
        queryFn: authApi.me,
        enabled: hasToken, //dont call this api without a token
        retry: false,
    })

    return {
        user: me.data,
        isLoading: me.isLoading,
        mustLogin: !hasToken || me.isError,
        logout: async () => {
            const refresh = tokenStore.refresh
            if (refresh) await authApi.logout(refresh).catch(() => {})// log out locally even if the server fails
            tokenStore.clear()
            navigate('/login', {replace: true})
        },
    }
}