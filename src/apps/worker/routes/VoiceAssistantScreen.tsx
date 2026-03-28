import { useState } from 'react'

export default function VoiceAssistantScreen() {
  const [status, setStatus] = useState<'idle' | 'listening' | 'error'>('idle')

  return (
    <main className="mx-auto max-w-md px-4 pb-24 pt-4">
      <h1 className="text-2xl font-black">Voice Assistant</h1>
      <p className="mt-2 text-sm text-slate-700">Commands: नौकरी खोजो, मेरा काम दिखाओ, घर जाओ</p>

      <div className="card-surface mt-4 p-5 text-center">
        <div className={`mx-auto mb-3 h-24 w-24 rounded-full ${status === 'listening' ? 'animate-pulse bg-worker-primary' : 'bg-slate-300'}`} />
        <p className="font-semibold">
          {status === 'idle' ? 'Tap to start listening' : status === 'listening' ? 'Listening...' : 'फिर से बोलें'}
        </p>
        <div className="mt-4 flex justify-center gap-2">
          <button type="button" onClick={() => setStatus('listening')} className="touch-target-48 rounded-lg bg-worker-primary px-3 py-2 text-white">
            Start
          </button>
          <button type="button" onClick={() => setStatus('error')} className="touch-target-48 rounded-lg bg-red-600 px-3 py-2 text-white">
            Error Test
          </button>
          <button type="button" onClick={() => setStatus('idle')} className="touch-target-48 rounded-lg border px-3 py-2">
            Reset
          </button>
        </div>
      </div>
    </main>
  )
}
