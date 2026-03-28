/* KaamSetu — main.js */

// ─── CSRF TOKEN ──────────────────────────────────────────────
function getCookie(name) {
  let val = null;
  document.cookie.split(';').forEach(c => {
    c = c.trim();
    if (c.startsWith(name + '=')) val = decodeURIComponent(c.slice(name.length + 1));
  });
  return val;
}

// ─── APPLY TO JOB ────────────────────────────────────────────
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.apply-btn');
  if (!btn) return;
  e.preventDefault();
  const jobId = btn.dataset.jobId;
  if (btn.disabled) return;
  btn.disabled = true;
  btn.textContent = '⏳';
  fetch(`/jobs/apply/${jobId}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' }
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      btn.textContent = '✅';
      btn.style.background = '#16a34a';
      btn.closest('.job-card')?.querySelector('.applied-badge')?.remove();
      const badge = document.createElement('div');
      badge.className = 'applied-badge'; badge.textContent = 'Applied';
      btn.closest('.job-card')?.prepend(badge);
      showToast('Applied! 🎉', 'success');
    } else {
      btn.disabled = false; btn.textContent = '👆 Apply';
      showToast(data.error || 'Could not apply', 'error');
    }
  })
  .catch(() => { btn.disabled = false; btn.textContent = '👆 Apply'; });
});

// ─── HIRE WORKER ─────────────────────────────────────────────
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.hire-btn');
  if (!btn) return;
  e.preventDefault();
  if (!confirm('Hire this worker?')) return;
  const appId = btn.dataset.appId;
  btn.disabled = true; btn.textContent = 'Hiring...';
  fetch(`/contractor/hire/${appId}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      btn.textContent = '✅ Hired';
      btn.style.background = '#16a34a';
      btn.closest('.applicant-card')?.classList.add('past-collab');
      showToast('Worker hired! SMS sent. 🎉', 'success');
    } else {
      btn.disabled = false; btn.textContent = 'Hire';
      showToast(data.error || 'Error', 'error');
    }
  });
});

// ─── FAVOURITE TOGGLE ────────────────────────────────────────
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.fav-btn');
  if (!btn) return;
  e.preventDefault();
  const workerId = btn.dataset.workerId;
  fetch(`/contractor/favourite/${workerId}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  })
  .then(r => r.json())
  .then(data => {
    btn.textContent = data.favourited ? '❤️' : '🤍';
    showToast(data.favourited ? 'Added to favourites' : 'Removed from favourites', 'info');
  });
});

// ─── STAR RATING UI ──────────────────────────────────────────
document.querySelectorAll('.star-input').forEach(star => {
  star.addEventListener('click', function() {
    const val = this.dataset.val;
    const group = this.closest('.star-group');
    const input = group.querySelector('input[type=hidden]');
    if (input) input.value = val;
    group.querySelectorAll('.star-input').forEach(s => {
      s.classList.toggle('selected', parseInt(s.dataset.val) <= parseInt(val));
    });
  });
  star.addEventListener('mouseover', function() {
    const val = parseInt(this.dataset.val);
    this.closest('.star-group').querySelectorAll('.star-input').forEach(s => {
      s.style.color = parseInt(s.dataset.val) <= val ? 'var(--amber)' : '#d1ccc7';
    });
  });
  star.addEventListener('mouseout', function() {
    const group = this.closest('.star-group');
    const selected = parseInt(group.querySelector('input[type=hidden]')?.value || 0);
    group.querySelectorAll('.star-input').forEach(s => {
      s.style.color = parseInt(s.dataset.val) <= selected ? 'var(--amber)' : '#d1ccc7';
    });
  });
});

// ─── GEOLOCATION ─────────────────────────────────────────────
function getUserLocation(onSuccess, onError) {
  if (!navigator.geolocation) { if (onError) onError('Not supported'); return; }
  navigator.geolocation.getCurrentPosition(
    pos => onSuccess(pos.coords.latitude, pos.coords.longitude),
    err => { if (onError) onError(err.message); },
    { timeout: 8000 }
  );
}

// Auto-fill location fields
document.querySelectorAll('[data-get-location]').forEach(btn => {
  btn.addEventListener('click', function() {
    this.textContent = '📍 Getting...';
    getUserLocation(
      (lat, lng) => {
        const form = this.closest('form');
        const latInput = form?.querySelector('[name=latitude]');
        const lngInput = form?.querySelector('[name=longitude]');
        if (latInput) latInput.value = lat.toFixed(6);
        if (lngInput) lngInput.value = lng.toFixed(6);
        this.textContent = '📍 Location Set ✓';
        this.style.background = 'var(--green)';
        showToast('Location captured!', 'success');
      },
      () => { this.textContent = '📍 Get Location'; showToast('Could not get location', 'error'); }
    );
  });
});

// ─── VOICE NAVIGATION (Worker UI) ─────────────────────────────
let recognition = null;
const voiceBtn = document.querySelector('.voice-btn');
if (voiceBtn) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'hi-IN';
    recognition.interimResults = false;

    voiceBtn.addEventListener('click', () => {
      if (voiceBtn.classList.contains('listening')) {
        recognition.stop(); voiceBtn.classList.remove('listening'); voiceBtn.textContent = '🎤';
      } else {
        recognition.start(); voiceBtn.classList.add('listening'); voiceBtn.textContent = '🔴';
      }
    });

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.toLowerCase();
      voiceBtn.classList.remove('listening'); voiceBtn.textContent = '🎤';
      handleVoiceCommand(transcript);
    };
    recognition.onerror = () => { voiceBtn.classList.remove('listening'); voiceBtn.textContent = '🎤'; };
  } else {
    voiceBtn.style.display = 'none';
  }
}

function handleVoiceCommand(cmd) {
  speak(`You said: ${cmd}`);
  if (cmd.includes('job') || cmd.includes('kaam')) {
    window.location.href = '/worker/feed/';
  } else if (cmd.includes('profile') || cmd.includes('profile')) {
    window.location.href = '/worker/profile/';
  } else if (cmd.includes('apply') || cmd.includes('lagao')) {
    const firstApply = document.querySelector('.apply-btn:not([disabled])');
    if (firstApply) { firstApply.click(); speak('Applied to first job'); }
  }
}

function speak(text) {
  if ('speechSynthesis' in window) {
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = 'hi-IN'; utt.rate = 0.9;
    window.speechSynthesis.speak(utt);
  }
}

// ─── READ JOB ALOUD ──────────────────────────────────────────
document.querySelectorAll('.read-job-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const card = this.closest('.job-card');
    const rate = card.querySelector('.job-card-rate')?.textContent?.trim();
    const loc = card.querySelector('.job-card-location')?.textContent?.trim();
    const dist = card.querySelector('.job-card-distance')?.textContent?.trim();
    speak(`Job available. Daily rate ${rate}. Location: ${loc}. ${dist || ''}`);
  });
});

// ─── TOAST NOTIFICATIONS ─────────────────────────────────────
function showToast(msg, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = 'position:fixed;top:1rem;right:1rem;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  const colors = { success: '#16a34a', error: '#dc2626', info: '#2563eb', warning: '#f59e0b' };
  toast.style.cssText = `background:${colors[type]||colors.info};color:white;padding:0.75rem 1.25rem;border-radius:10px;font-size:0.9rem;font-weight:600;box-shadow:0 4px 16px rgba(0,0,0,0.2);animation:slideIn 0.2s ease;max-width:300px;`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// ─── URGENT JOB PULSE ────────────────────────────────────────
document.querySelectorAll('.job-card.urgent').forEach(card => {
  card.style.animation = 'urgentPulse 2s infinite';
});

const style = document.createElement('style');
style.textContent = `
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes urgentPulse { 0%,100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.2); } 50% { box-shadow: 0 0 0 6px rgba(220,38,38,0.08); } }
`;
document.head.appendChild(style);
