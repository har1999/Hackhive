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
    <main className="mx-auto max-w-md px-4 pb-24 pt-4">
      <h1 className="mb-3 text-2xl font-black">My Jobs</h1>
      <div className="mb-4 flex gap-2">
        {tabs.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setTab(item.id)}
            className={`touch-target-48 rounded-lg border px-3 py-2 text-sm ${tab === item.id ? 'border-worker-primary bg-teal-50 font-bold' : 'border-slate-300'}`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === 'active' ? (
        <article className="card-surface p-4">
          <h2 className="text-lg font-bold">Plumbing Repair - Site B7</h2>
          <p className="text-sm text-slate-600">Mark complete with photo proof</p>
          <label className="mt-3 block rounded-lg border border-dashed border-slate-400 p-3 text-center">
            Upload completion photo
            <input accept="image/*" capture="environment" className="hidden" onChange={onImageChange} type="file" />
          </label>
          {compressedSize ? <p className="mt-2 text-sm">Compressed photo: {compressedSize} KB</p> : null}
          <button type="button" className="touch-target-48 mt-3 w-full rounded-lg bg-worker-success p-3 font-bold text-white">
            Mark Complete
          </button>
        </article>
      ) : null}

      {tab !== 'active' ? <p className="card-surface p-4">No jobs in this section yet.</p> : null}
    </main>
  )
}
