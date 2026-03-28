import { useState } from 'react'
import { SKILL_OPTIONS } from '../../../shared/constants/skills'

export default function PostJob() {
  const [skill, setSkill] = useState('plumbing')
  const [radius, setRadius] = useState(5)
  const [wage, setWage] = useState(800)

  return (
    <main className="p-6">
      <h1 className="mb-4 text-2xl font-black text-contractor-primary">Post New Job</h1>

      <section className="card-surface mb-4 p-4">
        <h2 className="mb-2 text-lg font-bold">1. Job Type</h2>
        <div className="grid grid-cols-2 gap-2 md:grid-cols-3">
          {SKILL_OPTIONS.map((item) => (
            <button
              type="button"
              key={item.id}
              onClick={() => setSkill(item.id)}
              className={`touch-target-48 rounded-lg border p-3 text-left ${skill === item.id ? 'border-contractor-primary bg-blue-50' : 'border-slate-300'}`}
            >
              {item.icon} {item.label}
            </button>
          ))}
        </div>
      </section>

      <section className="card-surface mb-4 p-4">
        <h2 className="mb-2 text-lg font-bold">2. Location Radius</h2>
        <div className="flex gap-2">
          {[2, 5, 10, 20].map((value) => (
            <button key={value} type="button" onClick={() => setRadius(value)} className={`touch-target-48 rounded-lg border px-3 ${radius === value ? 'border-contractor-primary bg-blue-50 font-bold' : 'border-slate-300'}`}>
              {value} km
            </button>
          ))}
        </div>
      </section>

      <section className="card-surface mb-4 p-4">
        <h2 className="mb-2 text-lg font-bold">3. Wage (Market Suggestion)</h2>
        <input type="range" min={350} max={1800} step={50} value={wage} onChange={(event) => setWage(Number(event.target.value))} className="w-full" />
        <p className="text-lg font-bold">₹{wage}/day</p>
      </section>

      <button type="button" className="touch-target-48 rounded-lg bg-contractor-primary px-4 py-3 font-semibold text-white">
        Publish Job
      </button>
    </main>
  )
}
