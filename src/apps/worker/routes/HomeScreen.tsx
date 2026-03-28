import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { LanguageSwitcher } from '../../../shared/components/LanguageSwitcher'
import { useNetworkStatus } from '../hooks/useNetworkStatus'

export default function HomeScreen() {
  const { t } = useTranslation()
  const networkStatus = useNetworkStatus()

  return (
    <main className="mx-auto max-w-md px-4 pb-28 pt-4">
      <header className="mb-4 flex items-center justify-between">
        <button type="button" className="touch-target-48 rounded-full border border-emerald-200 bg-white px-3">🔊</button>
        <h1 className="text-xl font-extrabold tracking-tight">नमस्ते, राम</h1>
        <div className="flex items-center gap-2">
          <LanguageSwitcher />
          <button type="button" className="touch-target-48 rounded-full border border-emerald-200 bg-white px-3">👤</button>
        </div>
      </header>

      {networkStatus !== 'online' ? (
        <div className="rise-in mb-4 rounded-xl border border-amber-400 bg-amber-50 p-3 text-sm font-semibold text-amber-900" aria-live="polite">
          {networkStatus === 'offline' ? t('offline.message') : 'Slow network detected. Lite mode active.'}
        </div>
      ) : null}

      <section className="card-surface rise-in mb-4 overflow-hidden p-4">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-base font-bold uppercase tracking-wide text-worker-primary">Live Alerts</p>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-700">Nearby</span>
        </div>
        <p className="text-2xl font-black">🔔 2 नई नौकरी</p>
        <p className="mt-1 text-sm text-slate-600">2km के अंदर पलंबर और इलेक्ट्रिकल काम उपलब्ध</p>
      </section>

      <section className="stagger-list grid grid-cols-2 gap-3">
        <Link className="card-surface touch-target-48 rise-in rounded-2xl p-4 text-center transition-transform hover:-translate-y-1" to="/worker/jobs">
          <div className="text-3xl">🔍</div>
          <p className="mt-2 text-base font-extrabold">नौकरी खोजें</p>
          <p className="text-xs text-slate-500">आज की नई पोस्ट</p>
        </Link>
        <Link className="card-surface touch-target-48 rise-in rounded-2xl p-4 text-center transition-transform hover:-translate-y-1" to="/worker/my-jobs">
          <div className="text-3xl">📋</div>
          <p className="mt-2 text-base font-extrabold">मेरी काम</p>
          <p className="text-xs text-slate-500">एक्टिव और पूरा</p>
        </Link>
        <Link className="card-surface touch-target-48 rise-in rounded-2xl p-4 text-center transition-transform hover:-translate-y-1" to="/worker/profile">
          <div className="text-3xl">⭐</div>
          <p className="mt-2 text-base font-extrabold">मेरी रेटिंग</p>
          <p className="text-xs text-slate-500">विश्वास स्कोर</p>
        </Link>
        <Link className="card-surface touch-target-48 rise-in rounded-2xl p-4 text-center transition-transform hover:-translate-y-1" to="/worker/assistant">
          <div className="text-3xl">💰</div>
          <p className="mt-2 text-base font-extrabold">कमाई देखें</p>
          <p className="text-xs text-slate-500">साप्ताहिक रिपोर्ट</p>
        </Link>
      </section>

      <button type="button" className="rise-in mt-4 w-full rounded-2xl bg-gradient-to-r from-worker-primary to-teal-500 px-4 py-4 text-lg font-black text-white shadow-lg">
        🎤 {t('voice.search')}
      </button>
    </main>
  )
}
