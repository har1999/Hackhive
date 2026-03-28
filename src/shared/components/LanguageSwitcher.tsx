import type { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'

const LANGUAGE_OPTIONS = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'Hindi' },
  { code: 'ta', label: 'Tamil' },
  { code: 'te', label: 'Telugu' },
  { code: 'mr', label: 'Marathi' },
] as const

export const LanguageSwitcher = () => {
  const { i18n } = useTranslation()

  const handleChange = async (event: ChangeEvent<HTMLSelectElement>) => {
    const selected = event.target.value
    localStorage.setItem('kaamsetu.language', selected)
    await i18n.changeLanguage(selected)
  }

  return (
    <label className="inline-flex items-center gap-1 text-xs font-semibold text-slate-700" htmlFor="language-select">
      <span aria-hidden="true">🌐</span>
      <span className="sr-only">Language</span>
      <select
        id="language-select"
        value={i18n.resolvedLanguage ?? 'hi'}
        onChange={handleChange}
        className="rounded-md border border-slate-300 bg-white px-2 py-1 text-xs font-bold"
      >
        {LANGUAGE_OPTIONS.map((option) => (
          <option key={option.code} value={option.code}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  )
}
