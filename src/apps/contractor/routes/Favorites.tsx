const workers = [
  { id: 'w1', name: 'राम प्रसाद', skill: 'Plumbing', available: true },
  { id: 'w2', name: 'सुनील यादव', skill: 'Electrical', available: false },
]

export default function Favorites() {
  return (
    <main className="px-6 pb-10 pt-6">
      <h1 className="mb-1 text-3xl font-black tracking-tight text-contractor-primary">Favorite Workers</h1>
      <p className="mb-4 text-sm text-slate-600">Your trusted workers with one-tap rehire.</p>
      <div className="grid gap-3 md:grid-cols-2">
        {workers.map((worker) => (
          <article key={worker.id} className="card-surface rise-in p-4">
            <p className="font-black">⭐ {worker.name}</p>
            <p className="text-sm text-slate-600">{worker.skill}</p>
            <p className={`text-sm ${worker.available ? 'text-green-700' : 'text-slate-500'}`}>
              {worker.available ? 'Available now' : 'Busy'}
            </p>
            <button type="button" className="touch-target-48 mt-3 rounded-lg bg-gradient-to-r from-contractor-primary to-blue-500 px-3 py-2 font-bold text-white">
              Rehire
            </button>
          </article>
        ))}
      </div>
    </main>
  )
}
