import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'

const COMMANDS: Record<string, string | number> = {
  'नौकरी खोजो': '/worker/jobs',
  'मेरा काम': '/worker/my-jobs',
  'मेरा काम दिखाओ': '/worker/my-jobs',
  'घर जाओ': '/worker',
  वापस: -1,
}

const normalize = (value: string) => value.trim().replace(/\s+/g, ' ')

export const useVoiceNavigation = () => {
  const navigate = useNavigate()
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition()

  useEffect(() => {
    const key = normalize(transcript)
    const route = COMMANDS[key]
    if (!route) {
      return
    }

    if (typeof route === 'string') {
      navigate(route)
    } else {
      navigate(route)
    }

    resetTranscript()
  }, [navigate, resetTranscript, transcript])

  const start = () => {
    if (!browserSupportsSpeechRecognition) {
      return false
    }

    SpeechRecognition.startListening({ language: 'hi-IN' })
    return true
  }

  const stop = () => SpeechRecognition.stopListening()

  return { start, stop, browserSupportsSpeechRecognition, transcript }
}
