const workers = [
  { id: 'w1', name: 'राम प्रसाद', skill: 'Plumbing', available: true },
  { id: 'w2', name: 'सुनील यादव', skill: 'Electrical', available: false },
]

export default function Favorites() {
  return (
    <main className="p-6">
      <h1 className="mb-4 text-2xl font-black text-contractor-primary">Favorite Workers</h1>
      <div className="grid gap-3 md:grid-cols-2">
        {workers.map((worker) => (
          <article key={worker.id} className="card-surface p-4">
            <p className="font-bold">⭐ {worker.name}</p>
            <p>{worker.skill}</p>
            <p className={`text-sm ${worker.available ? 'text-green-700' : 'text-slate-500'}`}>
              {worker.available ? 'Available now' : 'Busy'}
            </p>
            <button type="button" className="touch-target-48 mt-2 rounded-lg bg-contractor-primary px-3 py-2 text-white">
              Rehire
            </button>
          </article>
        ))}
      </div>
    </main>
  )
}
