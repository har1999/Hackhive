import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { SKILL_OPTIONS } from '../../../shared/constants/skills'
import { api } from '../../../shared/api/client'
import { getCurrentLocation } from '../../../shared/utils/geolocation'
import { offlineQueue } from '../../../shared/api/offlineQueue'

export default function JobSearchScreen() {
  const { t } = useTranslation()
  const [skill, setSkill] = useState<string | undefined>()
  const [radius, setRadius] = useState(5)

  const jobsQuery = useQuery({
    queryKey: ['jobs', skill, radius],
    queryFn: async () => {
      const location = await getCurrentLocation()
      return api.searchJobs({ skill, location, radius })
    },
  })

  return (
    <main className="mx-auto max-w-md px-4 pb-28 pt-4">
      <h1 className="mb-1 text-3xl font-black tracking-tight">{t('job.search')}</h1>
      <p className="mb-4 text-sm text-slate-600">Radius and skill filters are optimized for low network mode.</p>

      <div className="card-surface mb-4 p-3">
        <p className="mb-2 text-xs font-bold uppercase tracking-wide text-worker-primary">Search Radius</p>
        <div className="flex gap-2">
        {[2, 5, 10].map((value) => (
          <button
            key={value}
            onClick={() => setRadius(value)}
            type="button"
            className={`touch-target-48 rounded-lg border px-3 ${radius === value ? 'border-worker-primary bg-teal-100 font-bold text-worker-primary' : 'border-slate-300 bg-white'}`}
          >
            {value} km
          </button>
        ))}
        </div>
      </div>

      <div className="card-surface mb-4 p-3">
        <p className="mb-2 text-xs font-bold uppercase tracking-wide text-worker-primary">Skill Type</p>
        <div className="grid grid-cols-3 gap-2">
        {SKILL_OPTIONS.map((item) => (
          <button
            type="button"
            key={item.id}
            onClick={() => setSkill(item.id)}
            className={`touch-target-48 rounded-xl border p-2 text-sm ${skill === item.id ? 'border-worker-primary bg-teal-100 font-bold text-worker-primary' : 'border-slate-300 bg-white'}`}
          >
            <div>{item.icon}</div>
            <div>{item.label}</div>
          </button>
        ))}
        </div>
      </div>

      <div className="space-y-3">
        {jobsQuery.data?.map((job) => (
          <article className="card-surface rise-in p-4" key={job.id}>
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-black text-worker-primary">₹{job.wage}/day</h2>
              {job.urgent ? <span className="rounded bg-red-100 px-2 py-1 text-xs font-bold text-red-700">Urgent</span> : null}
            </div>
            <p className="mt-1 text-base font-bold">{job.title}</p>
            <p className="text-sm text-slate-600">{job.distanceKm} km away • Skill: {job.skill}</p>
            <button
              onClick={() => offlineQueue.addJobApplication(job.id)}
              type="button"
              className="touch-target-48 mt-3 w-full rounded-xl bg-gradient-to-r from-worker-info to-blue-500 px-3 py-2 font-bold text-white"
            >
              {t('job.apply')}
            </button>
          </article>
        ))}

        {jobsQuery.data?.length === 0 ? (
          <p className="card-surface p-4 text-sm text-slate-600">No jobs available for this filter right now.</p>
        ) : null}
      </div>
    </main>
  )
}
