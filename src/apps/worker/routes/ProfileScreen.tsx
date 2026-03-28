import { useTranslation } from 'react-i18next'

export default function ProfileScreen() {
  const { t } = useTranslation()

  return (
    <main className="mx-auto max-w-md px-4 pb-24 pt-4">
      <div className="card-surface p-5 text-center">
        <div className="mx-auto mb-2 flex h-20 w-20 items-center justify-center rounded-full bg-slate-200 text-3xl">📸</div>
        <h1 className="text-2xl font-black">राम प्रसाद</h1>
        <div className="mt-4 rounded-2xl border border-slate-300 p-4">
          <p className="text-sm font-semibold uppercase tracking-wider">{t('trust.score')}</p>
          <p className="mt-1 text-4xl font-black">4.8</p>
          <p className="mt-1">⭐⭐⭐⭐⭐</p>
          <p className="mt-2 text-sm">23 काम पूरे, 15 दिन में</p>
        </div>
        <div className="mt-4 space-y-2 text-left">
          <div className="rounded-lg border p-3">💪 Skills - verified</div>
          <div className="rounded-lg border p-3">🏆 Badges</div>
          <div className="rounded-lg border p-3">📜 Work History</div>
        </div>
      </div>
    </main>
  )
}
