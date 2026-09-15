import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, RouterProvider } from 'react-router'

import { AuthCard } from './shared/ui'

import './index.css'


const router = createBrowserRouter(
  [
    { path: '*', element: <AuthCard title="Login Service">Coming soon...</AuthCard>}
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
