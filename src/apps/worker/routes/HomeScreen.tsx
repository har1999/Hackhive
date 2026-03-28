import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useNetworkStatus } from '../hooks/useNetworkStatus'

export default function HomeScreen() {
  const { t } = useTranslation()
  const networkStatus = useNetworkStatus()

  return (
    <main className="mx-auto max-w-md px-4 pb-24 pt-4">
      <header className="mb-4 flex items-center justify-between">
        <button type="button" className="touch-target-48 rounded-full border border-slate-300 px-3">🔊</button>
        <h1 className="text-xl font-bold">नमस्ते, राम</h1>
        <button type="button" className="touch-target-48 rounded-full border border-slate-300 px-3">👤</button>
      </header>

      {networkStatus !== 'online' ? (
        <div className="mb-4 rounded-xl border border-amber-400 bg-amber-50 p-3 text-sm font-semibold text-amber-900" aria-live="polite">
          {networkStatus === 'offline' ? t('offline.message') : 'Slow network detected. Lite mode active.'}
        </div>
      ) : null}

      <section className="card-surface mb-4 p-4">
        <p className="text-lg font-bold">🔔 2 नई नौकरी nearby</p>
      </section>

      <section className="grid grid-cols-2 gap-3">
        <Link className="card-surface touch-target-48 rounded-2xl p-4 text-center" to="/worker/jobs">
          <div className="text-3xl">🔍</div>
          <p className="mt-2 font-semibold">नौकरी खोजें</p>
        </Link>
        <Link className="card-surface touch-target-48 rounded-2xl p-4 text-center" to="/worker/my-jobs">
          <div className="text-3xl">📋</div>
          <p className="mt-2 font-semibold">मेरी काम</p>
        </Link>
        <Link className="card-surface touch-target-48 rounded-2xl p-4 text-center" to="/worker/profile">
          <div className="text-3xl">⭐</div>
          <p className="mt-2 font-semibold">मेरी रेटिंग</p>
        </Link>
        <Link className="card-surface touch-target-48 rounded-2xl p-4 text-center" to="/worker/assistant">
          <div className="text-3xl">💰</div>
          <p className="mt-2 font-semibold">कमाई देखें</p>
        </Link>
      </section>

      <button type="button" className="mt-4 w-full rounded-2xl bg-worker-primary px-4 py-4 text-lg font-bold text-white">
        🎤 {t('voice.search')}
      </button>
    </main>
  )
}
