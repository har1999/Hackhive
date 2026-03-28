declare module 'react-speech-recognition' {
  export type UseSpeechRecognitionResult = {
    transcript: string
    resetTranscript: () => void
    browserSupportsSpeechRecognition: boolean
  }

  const SpeechRecognition: {
    startListening: (options?: { language?: string }) => void
    stopListening: () => void
  }

  export const useSpeechRecognition: () => UseSpeechRecognitionResult
  export default SpeechRecognition
}
