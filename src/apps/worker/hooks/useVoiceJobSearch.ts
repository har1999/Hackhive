import { useMutation } from '@tanstack/react-query'
import { api } from '../../../shared/api/client'
import { getCurrentLocation } from '../../../shared/utils/geolocation'

const SKILL_DICT: Record<string, string> = {
  प्लंबर: 'plumbing',
  बिजली: 'electrical',
  बढ़ई: 'carpentry',
  पेंट: 'painting',
  मजदूर: 'labor',
}

export const useVoiceJobSearch = () => {
  const mutation = useMutation({
    mutationFn: async (transcript: string) => {
      const location = await getCurrentLocation()
      const skill = Object.entries(SKILL_DICT).find(([key]) => transcript.includes(key))?.[1]
      return api.searchJobs({ skill, location, radius: 5 })
    },
  })

  return mutation
}
