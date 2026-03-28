import { useState } from 'react'

export default function Broadcast() {
  const [message, setMessage] = useState('Urgent: Need 3 plumbers near Site B7, today 3 PM')

  return (
    <main className="px-6 pb-10 pt-6">
      <h1 className="mb-1 text-3xl font-black tracking-tight text-red-700">Emergency Broadcast</h1>
      <p className="mb-4 text-sm text-slate-600">Push urgent requirements instantly with SMS fallback.</p>
      <section className="card-surface rise-in border border-red-300 p-4">
        <label htmlFor="broadcast" className="mb-2 block font-semibold">Urgent message</label>
        <textarea id="broadcast" value={message} onChange={(event) => setMessage(event.target.value)} className="h-32 w-full rounded-lg border border-slate-300 p-3" />
        <div className="mt-3 flex gap-2">
          <button type="button" className="touch-target-48 rounded-lg bg-gradient-to-r from-red-700 to-red-500 px-4 py-2 font-bold text-white">Send Broadcast</button>
          <button type="button" className="touch-target-48 rounded-lg border border-slate-300 bg-white px-4 py-2 font-bold">SMS Fallback</button>
        </div>
      </section>

      <section className="mt-4 grid gap-3 md:grid-cols-3">
        <article className="card-surface p-4">
          <h2 className="text-xs uppercase tracking-wide text-slate-500">Delivered</h2>
          <p className="text-3xl font-black text-contractor-primary">14</p>
        </article>
        <article className="card-surface p-4">
          <h2 className="text-xs uppercase tracking-wide text-slate-500">Seen</h2>
          <p className="text-3xl font-black text-amber-600">8</p>
        </article>
        <article className="card-surface p-4">
          <h2 className="text-xs uppercase tracking-wide text-slate-500">Accepted</h2>
          <p className="text-3xl font-black text-green-700">3</p>
        </article>
      </section>
    </main>
  )
}
