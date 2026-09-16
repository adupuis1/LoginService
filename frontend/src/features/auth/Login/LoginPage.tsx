import { Link } from 'react-router'
import { AuthCard, Button, ErrorMessage, Field } from "../../../shared/ui";
import { useLoginViewModel } from "./useLoginViewModel";

export function LoginPage() {
    const vm = useLoginViewModel()

    return (
        <AuthCard title="Log in">
            <form onSubmit={vm.submit} className="grid gap-4">
                {vm.error && <ErrorMessage message={vm.error}/>}
                <Field
                    label="Username"
                    autoComplete="username"
                    autoFocus
                    value={vm.username}
                    onChange={(e) => vm.setUsername(e.target.value)}
                />
                <Field
                    label="Password"
                    type="password"
                    autoComplete="current-password"
                    value={vm.password}
                    onChange={(e) => vm.setPassword(e.target.value)}
                />
                <Button disabled={vm.isSubmitting}>{vm.isSubmitting ? 'Logging in...' : 'Login'}</Button>
                <p className="text-center text-sm text-zinc-500">
                    No account?{' '}
                    <Link to="/signup" className="font-medium text-zing-900 hover:underline">
                    Sign up
                    </Link>
                </p>
            </form>
        </AuthCard>
    )
}