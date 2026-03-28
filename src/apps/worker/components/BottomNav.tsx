import clsx from 'clsx'
import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { path: '/worker', icon: '🏠', label: 'Home' },
  { path: '/worker/jobs', icon: '🔍', label: 'Jobs' },
  { path: '/worker/my-jobs', icon: '📋', label: 'My Jobs' },
  { path: '/worker/profile', icon: '👤', label: 'Profile' },
]

export const BottomNav = () => {
  return (
    <nav className="glass-strip fixed bottom-3 left-3 right-3 z-40 mx-auto flex max-w-md justify-around rounded-2xl px-1 py-2 shadow-lg">
      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            clsx(
              'touch-target-48 flex w-20 flex-col items-center justify-center rounded-xl text-xs font-semibold text-slate-600 transition-all',
              isActive && 'bg-worker-primary text-white shadow-md'
            )
          }
        >
          <span aria-hidden="true">{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
