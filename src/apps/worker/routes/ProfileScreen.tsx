import { useTranslation } from 'react-i18next'

export default function ProfileScreen() {
  const { t } = useTranslation()

  return (
    <main className="mx-auto max-w-md px-4 pb-28 pt-4">
      <div className="card-surface rise-in overflow-hidden p-5 text-center">
        <div className="mx-auto mb-2 flex h-20 w-20 items-center justify-center rounded-full border-4 border-white bg-gradient-to-br from-emerald-100 to-amber-100 text-3xl shadow-md">📸</div>
        <h1 className="text-2xl font-black tracking-tight">राम प्रसाद</h1>
        <p className="text-sm text-slate-600">Plumbing • Electrical • Masonry</p>
        <div className="mt-4 rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-amber-50 p-4">
          <p className="text-sm font-semibold uppercase tracking-wider text-worker-primary">{t('trust.score')}</p>
          <p className="mt-1 text-5xl font-black text-worker-primary">4.8</p>
          <p className="mt-1">⭐⭐⭐⭐⭐</p>
          <p className="mt-2 text-sm">23 काम पूरे, 15 दिन में</p>
        </div>
        <div className="mt-4 space-y-2 text-left">
          <div className="rounded-xl border border-slate-300 bg-white p-3 font-semibold">💪 Skills - verified</div>
          <div className="rounded-xl border border-slate-300 bg-white p-3 font-semibold">🏆 Badges</div>
          <div className="rounded-xl border border-slate-300 bg-white p-3 font-semibold">📜 Work History</div>
        </div>
      </div>
    </main>
  )
}
