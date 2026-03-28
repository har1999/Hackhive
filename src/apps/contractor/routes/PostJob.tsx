import { useState } from 'react'
import { SKILL_OPTIONS } from '../../../shared/constants/skills'

export default function PostJob() {
  const [skill, setSkill] = useState('plumbing')
  const [radius, setRadius] = useState(5)
  const [wage, setWage] = useState(800)

  return (
    <main className="px-6 pb-10 pt-6">
      <h1 className="mb-1 text-3xl font-black tracking-tight text-contractor-primary">Post New Job</h1>
      <p className="mb-4 text-sm text-slate-600">Create a complete job card in under 60 seconds.</p>

      <section className="card-surface rise-in mb-4 p-4">
        <h2 className="mb-2 text-lg font-black">1. Job Type</h2>
        <div className="grid grid-cols-2 gap-2 md:grid-cols-3">
          {SKILL_OPTIONS.map((item) => (
            <button
              type="button"
              key={item.id}
              onClick={() => setSkill(item.id)}
              className={`touch-target-48 rounded-xl border p-3 text-left font-semibold ${skill === item.id ? 'border-contractor-primary bg-blue-100 text-contractor-primary' : 'border-slate-300 bg-white'}`}
            >
              {item.icon} {item.label}
            </button>
          ))}
        </div>
      </section>

      <section className="card-surface rise-in mb-4 p-4">
        <h2 className="mb-2 text-lg font-black">2. Location Radius</h2>
        <div className="flex gap-2">
          {[2, 5, 10, 20].map((value) => (
            <button key={value} type="button" onClick={() => setRadius(value)} className={`touch-target-48 rounded-lg border px-3 ${radius === value ? 'border-contractor-primary bg-blue-100 font-bold text-contractor-primary' : 'border-slate-300 bg-white'}`}>
              {value} km
            </button>
          ))}
        </div>
      </section>

      <section className="card-surface rise-in mb-4 p-4">
        <h2 className="mb-2 text-lg font-black">3. Wage (Market Suggestion)</h2>
        <input type="range" min={350} max={1800} step={50} value={wage} onChange={(event) => setWage(Number(event.target.value))} className="w-full" />
        <p className="text-2xl font-black text-contractor-primary">₹{wage}/day</p>
      </section>

      <button type="button" className="touch-target-48 rounded-lg bg-gradient-to-r from-contractor-primary to-blue-500 px-4 py-3 font-black text-white shadow-lg">
        Publish Job
      </button>
    </main>
  )
}
