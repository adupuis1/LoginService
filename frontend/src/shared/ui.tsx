import type { ComponentProps, ReactNode } from 'react'

export function AuthCard({ title, children }: {title: string; children: ReactNode}) {
    return (
        <main className = "grid min-h-screen place-items-center bg-zinc-100 p-4">
            <div className="w-full max-w-sm rounded-2xl bg-white p-8 shadow-lg">
                <h1 className="mb-6 text-2xl font-semibold">{title}</h1>
                {children}
            </div>
        </main>
    )
}

export function Field({label, ...props }: {label: string } & ComponentProps<'input'>) {
    return (
        <label className="grid gap-1 text-sm font-medium">
            {label}
            <input
            {...props}
            className="rounded-lg border border-zinc-300 px-3 py-2 font-normal outline-none focus:border-zinc-900 focus:ring-2 focus:ring-zinc-900/10"/>
        </label>
    )
}

export function Button(props: ComponentProps<'button'>) {
    return (
        <button
        {...props}
        className="w-full rounded-lg bg-zinc-900 px-3 py-2 font-medium text-white hover:bg-zinc-700 disabled:opacity-50"
        />
    )
}

export function ErrorMessage({ message }: {message?: string }) {
    if(!message) return null
    return (
        <p role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {message}
        </p>
    )
}