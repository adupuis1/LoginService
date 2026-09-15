import { Navigate } from "react-router";
import { AuthCard, Button } from "../../../shared/ui";
import { useAccountViewModel } from "./useAccountViewModel";

export function AccountPage() {
    const vm = useAccountViewModel()

    if(vm.mustLogin) return <Navigate to="/login" replace />
    if(vm.isLoading || !vm.user) return <p className="p-8 text zinc-500">Loading...</p>


    return (
        <AuthCard title={`Hi, ${vm.user.username}`}>
            <div className="grid gap-4">
                {vm.user.is_superuser && (
                    <span className="w-fit rounded-full bg-zinc-900 px-2 py-0.5 text-xs text-white">Admin</span>
                )}
                <p className="text-sm text-zinc-500">You're logged in.</p>
                <Button onClick={vm.logout}>Log out</Button>
            </div>
        </AuthCard>
    )
}