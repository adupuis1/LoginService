import { Link } from 'react-router'
import { AuthCard, Button, ErrorMessage, Field } from '../../../shared/ui'
import { useSignupViewModel } from './useSignupViewModel.ts'

export function SignupPage() {
  const vm = useSignupViewModel()

  return (
    <AuthCard title="Create account">
      <form onSubmit={vm.submit} className="grid gap-4">
        {vm.error && <ErrorMessage message={vm.error} />}
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
          autoComplete="new-password"
          value={vm.password}
          onChange={(e) => vm.setPassword(e.target.value)}
        />
        <Field
          label="Confirm password"
          type="password"
          autoComplete="new-password"
          value={vm.confirm}
          onChange={(e) => vm.setConfirm(e.target.value)}
        />
        <Button disabled={vm.isSubmitting}>{vm.isSubmitting ? 'Creating…' : 'Create account'}</Button>
        <p className="text-center text-sm text-zinc-500">
          Have an account?{' '}
          <Link to="/login" className="font-medium text-zinc-900 hover:underline">
            Log in
          </Link>
        </p>
      </form>
    </AuthCard>
  )
}