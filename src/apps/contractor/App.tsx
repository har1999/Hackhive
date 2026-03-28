import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import { LanguageSwitcher } from '../../shared/components/LanguageSwitcher'
import Dashboard from './routes/Dashboard'
import PostJob from './routes/PostJob'
import Applicants from './routes/Applicants'
import Broadcast from './routes/Broadcast'
import Favorites from './routes/Favorites'

const links = [
  { to: '/contractor', label: 'Dashboard' },
  { to: '/contractor/post-job', label: 'Post Job' },
  { to: '/contractor/applicants', label: 'Applicants' },
  { to: '/contractor/broadcast', label: 'Broadcast' },
  { to: '/contractor/favorites', label: 'Favorites' },
]

export default function ContractorApp() {
  return (
    <div className="contractor-shell">
      <nav className="glass-strip sticky top-0 z-20 mx-3 mt-3 flex flex-wrap items-center gap-2 rounded-2xl px-4 py-3 shadow-sm">
        <p className="mr-2 text-sm font-black uppercase tracking-wide text-contractor-primary">KaamSetu Pro</p>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/contractor'}
            className={({ isActive }) =>
              `rounded-md px-3 py-2 text-sm font-semibold transition-colors ${isActive ? 'bg-contractor-primary text-white' : 'text-slate-700 hover:bg-slate-100'}`
            }
          >
            {link.label}
          </NavLink>
        ))}
        <div className="ml-auto">
          <LanguageSwitcher />
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/post-job" element={<PostJob />} />
        <Route path="/applicants" element={<Applicants />} />
        <Route path="/broadcast" element={<Broadcast />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="*" element={<Navigate to="/contractor" replace />} />
      </Routes>
    </div>
  )
}
