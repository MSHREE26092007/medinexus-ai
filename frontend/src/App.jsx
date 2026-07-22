import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'

export default function App() {
  const [view, setView] = useState('dashboard')

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar active={view} onNavigate={setView} />
      <main className="flex-1 overflow-y-auto">
        {/* Dashboard doubles as the patient list view for Phase 1 */}
        <Dashboard key={view} />
      </main>
    </div>
  )
}
