import { useState } from 'react'
import type { ChangeEvent } from 'react'
import { compressJobPhoto } from '../../../shared/utils/compressImage'

const tabs = [
  { id: 'active', label: '🟢 Active' },
  { id: 'completed', label: '✅ Completed' },
  { id: 'applied', label: '🟡 Applied' },
] as const

export default function MyJobsScreen() {
  const [tab, setTab] = useState<(typeof tabs)[number]['id']>('active')
  const [compressedSize, setCompressedSize] = useState<number | null>(null)

  const onImageChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }

    const compressed = await compressJobPhoto(file)
    setCompressedSize(Math.round(compressed.size / 1024))
  }

  return (
    <main className="mx-auto max-w-md px-4 pb-28 pt-4">
      <h1 className="mb-1 text-3xl font-black tracking-tight">My Jobs</h1>
      <p className="mb-4 text-sm text-slate-600">Track active, completed, and applied work in one place.</p>

      <div className="card-surface mb-4 flex gap-2 p-2">
        {tabs.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setTab(item.id)}
            className={`touch-target-48 flex-1 rounded-lg border px-2 py-2 text-sm ${tab === item.id ? 'border-worker-primary bg-teal-100 font-bold text-worker-primary' : 'border-slate-300 bg-white'}`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === 'active' ? (
        <article className="card-surface rise-in p-4">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-lg font-black">Plumbing Repair - Site B7</h2>
            <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-bold text-emerald-700">Active</span>
          </div>
          <p className="text-sm text-slate-600">Mark complete with photo proof</p>
          <label className="mt-3 block rounded-xl border-2 border-dashed border-slate-400 p-4 text-center font-semibold">
            Upload completion photo
            <input accept="image/*" capture="environment" className="hidden" onChange={onImageChange} type="file" />
          </label>
          {compressedSize ? <p className="mt-2 text-sm font-semibold text-emerald-700">Compressed photo: {compressedSize} KB</p> : null}
          <button type="button" className="touch-target-48 mt-3 w-full rounded-xl bg-gradient-to-r from-worker-success to-emerald-500 p-3 font-black text-white">
            Mark Complete
          </button>
        </article>
      ) : null}

      {tab !== 'active' ? <p className="card-surface rise-in p-4 text-sm text-slate-600">No jobs in this section yet.</p> : null}
    </main>
  )
}
