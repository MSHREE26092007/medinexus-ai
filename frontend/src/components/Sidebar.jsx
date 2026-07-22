const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'patients', label: 'Patients', icon: '🧑‍⚕️' },
  { id: 'monitoring', label: 'Live Monitoring', icon: '📡', soon: true },
  { id: 'knowledge', label: 'Knowledge Base', icon: '📚', soon: true },
  { id: 'reports', label: 'Reports', icon: '📄', soon: true },
  { id: 'copilot', label: 'AI Copilot', icon: '🤖', soon: true },
]

export default function Sidebar({ active, onNavigate }) {
  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col bg-slate-900 text-slate-300">
      <div className="flex items-center gap-3 px-6 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-500 text-xl font-bold text-white">
          M
        </div>
        <div>
          <h1 className="text-lg font-bold text-white">MediNexus AI</h1>
          <p className="text-xs text-slate-400">Clinical Intelligence</p>
        </div>
      </div>

      <nav className="mt-4 flex-1 space-y-1 px-3">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            onClick={() => !item.soon && onNavigate(item.id)}
            disabled={item.soon}
            className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm font-medium transition
              ${active === item.id
                ? 'bg-teal-500/15 text-teal-400'
                : item.soon
                  ? 'cursor-not-allowed text-slate-600'
                  : 'hover:bg-slate-800 hover:text-white'}`}
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
            {item.soon && (
              <span className="ml-auto rounded bg-slate-800 px-1.5 py-0.5 text-[10px] uppercase text-slate-500">
                soon
              </span>
            )}
          </button>
        ))}
      </nav>

      <div className="border-t border-slate-800 px-6 py-4 text-xs text-slate-500">
        <span className="mr-2 inline-block h-2 w-2 rounded-full bg-emerald-400" />
        Offline mode · Local LLM
      </div>
    </aside>
  )
}
