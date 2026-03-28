type IconButtonProps = {
  icon: string
  label: string
  onClick: () => void
}

export const IconButton = ({ icon, label, onClick }: IconButtonProps) => {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="touch-target-48 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-3 text-left font-semibold"
      type="button"
    >
      <span aria-hidden="true">{icon}</span>
      <span>{label}</span>
    </button>
  )
}
