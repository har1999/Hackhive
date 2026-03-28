import { useState } from 'react'

export default function Broadcast() {
  const [message, setMessage] = useState('Urgent: Need 3 plumbers near Site B7, today 3 PM')

  return (
    <main className="p-6">
      <h1 className="mb-4 text-2xl font-black text-red-700">Emergency Broadcast</h1>
      <section className="card-surface border-red-300 p-4">
        <label htmlFor="broadcast" className="mb-2 block font-semibold">Urgent message</label>
        <textarea id="broadcast" value={message} onChange={(event) => setMessage(event.target.value)} className="h-32 w-full rounded-lg border border-slate-300 p-3" />
        <div className="mt-3 flex gap-2">
          <button type="button" className="touch-target-48 rounded-lg bg-red-700 px-4 py-2 text-white">Send Broadcast</button>
          <button type="button" className="touch-target-48 rounded-lg border border-slate-300 px-4 py-2">SMS Fallback</button>
        </div>
      </section>
      <section className="mt-4 rounded-xl border border-slate-300 bg-white p-4">
        <h2 className="mb-2 font-bold">Delivery Status</h2>
        <p>Delivered: 14</p>
        <p>Seen: 8</p>
        <p>Accepted: 3</p>
      </section>
    </main>
  )
}
