import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import { resources } from './resources'

const preferredLanguage = localStorage.getItem('kaamsetu.language') ?? 'hi'

i18n.use(initReactI18next).init({
  resources,
  lng: preferredLanguage,
  fallbackLng: 'hi',
  interpolation: {
    escapeValue: false,
  },
})

export default i18n
