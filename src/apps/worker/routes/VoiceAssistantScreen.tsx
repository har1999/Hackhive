import { useState } from 'react'

export default function VoiceAssistantScreen() {
  const [status, setStatus] = useState<'idle' | 'listening' | 'error'>('idle')

  return (
    <main className="mx-auto max-w-md px-4 pb-28 pt-4">
      <h1 className="text-3xl font-black tracking-tight">Voice Assistant</h1>
      <p className="mt-2 text-sm text-slate-700">Commands: नौकरी खोजो, मेरा काम दिखाओ, घर जाओ</p>

      <div className="card-surface rise-in mt-4 p-5 text-center">
        <div className={`mx-auto mb-3 h-24 w-24 rounded-full ${status === 'listening' ? 'voice-ping bg-worker-primary' : 'bg-slate-300'}`} />
        <p className="font-bold">
          {status === 'idle' ? 'Tap to start listening' : status === 'listening' ? 'Listening...' : 'फिर से बोलें'}
        </p>
        <div className="mt-4 grid grid-cols-3 gap-2">
          <button type="button" onClick={() => setStatus('listening')} className="touch-target-48 rounded-lg bg-worker-primary px-3 py-2 font-bold text-white">
            Start
          </button>
          <button type="button" onClick={() => setStatus('error')} className="touch-target-48 rounded-lg bg-red-600 px-3 py-2 font-bold text-white">
            Error Test
          </button>
          <button type="button" onClick={() => setStatus('idle')} className="touch-target-48 rounded-lg border border-slate-300 bg-white px-3 py-2 font-bold">
            Reset
          </button>
        </div>
      </div>
    </main>
  )
}
