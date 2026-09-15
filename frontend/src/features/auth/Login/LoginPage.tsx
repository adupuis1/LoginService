import { AuthCard, Button, ErrorMessage, Field } from "../../../shared/ui";
import { useLoginViewModel } from "./useLoginViewModel";

export function LoginPage() {
    const vm = useLoginViewModel()

    return (
        <AuthCard title="Log in">
            <form onSubmit={vm.submit} className="grid gap-4">
                <ErrorMessage message="{vm.error}" />
                <Field
                    label="Username"
                    autoComplete="username"
                    autoFocus
                    value={vm.username}
                    onChange={(e) => vm.setUsername(e.target.value)}
                />
                <Field
                    label="Password"
                    autoComplete="password"
                    autoFocus
                    value={vm.password}
                    onChange={(e) => vm.setPassword(e.target.value)}
                />
                <Button disabled={vm.isSubmitting}>{vm.isSubmitting ? 'Loggin in...' : 'Login'}</Button>
            </form>
        </AuthCard>
    )
}