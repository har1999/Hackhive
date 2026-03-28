const applicants = [
  { id: 'a1', name: 'राम प्रसाद', trust: 4.9, distance: '3km', wage: 450, note: 'Worked with you before' },
  { id: 'a2', name: 'रवि कुमार', trust: 4.5, distance: '5km', wage: 500, note: 'Available today' },
]

export default function Applicants() {
  return (
    <main className="px-6 pb-10 pt-6">
      <h1 className="mb-1 text-3xl font-black tracking-tight text-contractor-primary">Applicants</h1>
      <p className="mb-4 text-sm text-slate-600">Sort by trust score, distance, and expected wage to hire faster.</p>
      <div className="card-surface rise-in overflow-x-auto rounded-xl">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-100">
            <tr>
              <th className="p-3 text-xs uppercase tracking-wide text-slate-500">Worker</th>
              <th className="p-3 text-xs uppercase tracking-wide text-slate-500">Trust Score</th>
              <th className="p-3 text-xs uppercase tracking-wide text-slate-500">Distance</th>
              <th className="p-3 text-xs uppercase tracking-wide text-slate-500">Expected Wage</th>
              <th className="p-3 text-xs uppercase tracking-wide text-slate-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            {applicants.map((applicant) => (
              <tr key={applicant.id} className="border-t border-slate-200">
                <td className="p-3">
                  <p className="font-semibold">{applicant.name}</p>
                  <p className="text-xs text-slate-500">{applicant.note}</p>
                </td>
                <td className="p-3">{applicant.trust} ★</td>
                <td className="p-3">{applicant.distance}</td>
                <td className="p-3">₹{applicant.wage}/day</td>
                <td className="p-3">
                  <div className="flex gap-2">
                    <button type="button" className="touch-target-48 rounded bg-green-600 px-3 py-1 text-xs font-bold text-white">Hire</button>
                    <button type="button" className="touch-target-48 rounded bg-amber-500 px-3 py-1 text-xs font-bold text-white">Shortlist</button>
                    <button type="button" className="touch-target-48 rounded bg-red-600 px-3 py-1 text-xs font-bold text-white">Reject</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
