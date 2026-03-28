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
    <main className="mx-auto max-w-md px-4 pb-24 pt-4">
      <h1 className="mb-2 text-2xl font-black">{t('job.search')}</h1>
      <div className="mb-4 flex gap-2">
        {[2, 5, 10].map((value) => (
          <button
            key={value}
            onClick={() => setRadius(value)}
            type="button"
            className={`touch-target-48 rounded-lg border px-3 ${radius === value ? 'border-worker-primary bg-teal-50 font-bold' : 'border-slate-300'}`}
          >
            {value} km
          </button>
        ))}
      </div>

      <div className="mb-4 grid grid-cols-3 gap-2">
        {SKILL_OPTIONS.map((item) => (
          <button
            type="button"
            key={item.id}
            onClick={() => setSkill(item.id)}
            className={`touch-target-48 rounded-xl border p-2 text-sm ${skill === item.id ? 'border-worker-primary bg-teal-50' : 'border-slate-300 bg-white'}`}
          >
            <div>{item.icon}</div>
            <div>{item.label}</div>
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {jobsQuery.data?.map((job) => (
          <article className="card-surface p-3" key={job.id}>
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-black">₹{job.wage}/day</h2>
              {job.urgent ? <span className="rounded bg-red-100 px-2 py-1 text-xs font-bold text-red-700">Urgent</span> : null}
            </div>
            <p className="text-sm font-semibold">{job.title}</p>
            <p className="text-sm text-slate-600">{job.distanceKm} km away</p>
            <button
              onClick={() => offlineQueue.addJobApplication(job.id)}
              type="button"
              className="touch-target-48 mt-2 w-full rounded-lg bg-worker-info px-3 py-2 text-white"
            >
              {t('job.apply')}
            </button>
          </article>
        ))}
      </div>
    </main>
  )
}
