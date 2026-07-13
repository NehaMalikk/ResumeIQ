import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { LandingLayout } from '@/layouts/LandingLayout'
import { LandingPage } from '@/pages/LandingPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<LandingLayout />}>
          <Route index element={<LandingPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
