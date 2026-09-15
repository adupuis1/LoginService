import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router'
import { LoginPage } from './features/auth/Login/LoginPage'
import { AuthCard } from './shared/ui'

import './index.css'


const router = createBrowserRouter(
  [
    { path: '/login', element: <LoginPage />},
    { path: '/account', element: <AuthCard title="Account Page">Coming soon...</AuthCard>},
    { path: '/*', element: <Navigate to="/login" replace />}
  ],
  { basename : '/auth'}
)

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
