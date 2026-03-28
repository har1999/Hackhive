import type { Coordinates } from '../utils/geolocation'

export type Job = {
  id: string
  title: string
  wage: number
  distanceKm: number
  skill: string
  urgent: boolean
}

export type SearchInput = {
  skill?: string
  location: Coordinates
  radius: number
}

const mockJobs: Job[] = [
  { id: '1', title: 'Plumbing Repair', wage: 800, distanceKm: 2.1, skill: 'plumbing', urgent: true },
  { id: '2', title: 'Electrical Wiring', wage: 950, distanceKm: 4.6, skill: 'electrical', urgent: false },
  { id: '3', title: 'Brick Work', wage: 700, distanceKm: 3.2, skill: 'masonry', urgent: false },
]

export const api = {
  searchJobs: async (input: SearchInput): Promise<Job[]> => {
    await new Promise((resolve) => setTimeout(resolve, 500))
    return mockJobs.filter((job) => (!input.skill ? true : job.skill === input.skill))
  },

  applyForJob: async (jobId: string) => {
    await new Promise((resolve) => setTimeout(resolve, 350))
    return { ok: true, jobId }
  },
}
