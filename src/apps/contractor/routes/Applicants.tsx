const applicants = [
  { id: 'a1', name: 'राम प्रसाद', trust: 4.9, distance: '3km', wage: 450, note: 'Worked with you before' },
  { id: 'a2', name: 'रवि कुमार', trust: 4.5, distance: '5km', wage: 500, note: 'Available today' },
]

export default function Applicants() {
  return (
    <main className="p-6">
      <h1 className="mb-4 text-2xl font-black text-contractor-primary">Applicants</h1>
      <div className="overflow-x-auto rounded-xl border border-slate-300 bg-white">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="p-3">Worker</th>
              <th className="p-3">Trust Score</th>
              <th className="p-3">Distance</th>
              <th className="p-3">Expected Wage</th>
              <th className="p-3">Actions</th>
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
                    <button type="button" className="touch-target-48 rounded bg-green-600 px-3 py-1 text-xs text-white">Hire</button>
                    <button type="button" className="touch-target-48 rounded bg-amber-500 px-3 py-1 text-xs text-white">Shortlist</button>
                    <button type="button" className="touch-target-48 rounded bg-red-600 px-3 py-1 text-xs text-white">Reject</button>
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
