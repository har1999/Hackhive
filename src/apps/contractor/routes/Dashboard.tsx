import { Link } from 'react-router-dom'

const cards = [
  { label: 'Active Jobs', value: '3' },
  { label: 'Applicants', value: '12' },
  { label: 'Trust Score', value: '4.7★' },
]

export default function Dashboard() {
  return (
    <main className="px-6 pb-10 pt-6">
      <header className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-contractor-primary">Contractor Command Center</h1>
          <p className="text-sm text-slate-600">Monitor hiring velocity, trust, and urgent staffing in real time.</p>
        </div>
        <div className="flex items-center gap-2">
          <button type="button" className="touch-target-48 rounded-lg border border-slate-300 bg-white px-3">🔔</button>
          <button type="button" className="touch-target-48 rounded-lg border border-slate-300 bg-white px-3">👤</button>
        </div>
      </header>

      <section className="stagger-list mb-6 grid gap-3 md:grid-cols-3">
        {cards.map((card) => (
          <article className="card-surface rise-in p-4" key={card.label}>
            <p className="text-xs font-bold uppercase tracking-wide text-slate-500">{card.label}</p>
            <p className="text-3xl font-black text-contractor-primary">{card.value}</p>
          </article>
        ))}
      </section>

      <section className="mb-6 flex flex-wrap gap-2">
        <Link to="/contractor/post-job" className="touch-target-48 rounded-lg bg-gradient-to-r from-contractor-primary to-blue-500 px-4 py-2 font-bold text-white">+ Post New Job</Link>
        <Link to="/contractor/broadcast" className="touch-target-48 rounded-lg bg-gradient-to-r from-red-700 to-red-500 px-4 py-2 font-bold text-white">📢 Emergency Broadcast</Link>
        <Link to="/contractor/favorites" className="touch-target-48 rounded-lg border border-slate-300 bg-white px-4 py-2 font-bold">⭐ Favorites</Link>
      </section>

      <section className="space-y-3">
        <article className="card-surface rise-in p-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold">🏗️ Building Construction</h2>
            <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-bold text-blue-700">8 applicants</span>
          </div>
          <p className="text-sm text-slate-600">📍 2km away • ₹800/day • 7 days remaining</p>
        </article>
        <article className="card-surface rise-in p-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold">🔧 Plumbing Repair</h2>
            <span className="rounded bg-red-100 px-2 py-1 text-xs font-bold text-red-700">Urgent</span>
          </div>
          <p className="text-sm text-slate-600">📍 5km away • ₹500/fix</p>
        </article>
      </section>
    </main>
  )
}
