import { useState } from 'react'
import { useVoiceNavigation } from '../hooks/useVoiceNavigation'

export const VoiceFab = () => {
  const [message, setMessage] = useState('')
  const { start } = useVoiceNavigation()

  const handleClick = () => {
    const started = start()
    if (!started) {
      setMessage('Voice not supported. Use tap actions.')
      return
    }

    setMessage('Listening... बोलें')
    window.setTimeout(() => setMessage(''), 2500)
  }

  return (
    <div className="fixed bottom-24 right-4 z-30">
      <button
        aria-label="Start voice assistant"
        className="touch-target-48 voice-ping rounded-full border-4 border-white bg-worker-primary px-5 py-4 text-xl text-white shadow-panel"
        onClick={handleClick}
        type="button"
      >
        🎤
      </button>
      {message ? (
        <p aria-live="polite" className="rise-in mt-2 rounded-md bg-black/80 px-3 py-2 text-xs text-white">
          {message}
        </p>
      ) : null}
    </div>
  )
}
