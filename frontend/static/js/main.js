/* ============================================================
   BUSMASTER — Core JavaScript
   ============================================================ */

const API = {
  base: '/api',
  async get(url) {
    const res = await fetch(this.base + url);
    return res.json();
  },
  async post(url, data) {
    const res = await fetch(this.base + url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },
  async put(url, data) {
    const res = await fetch(this.base + url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },
  async delete(url) {
    const res = await fetch(this.base + url, { method: 'DELETE' });
    return res.json();
  }
};

// ── CLOCK ──────────────────────────────────────────────
function updateClock() {
  const el = document.getElementById('clock');
  if (el) {
    const now = new Date();
    el.textContent = now.toLocaleTimeString('en-US', { hour12: false });
  }
}
setInterval(updateClock, 1000);
updateClock();

// ── TOAST ──────────────────────────────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const icons = { success: '✓', error: '✕', info: '!' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span style="font-size:16px;font-weight:700">${icons[type]}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ── MODAL ──────────────────────────────────────────────
function openModal(title, bodyHTML) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = bodyHTML;
  document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  document.getElementById('modal-body').innerHTML = '';
}

document.getElementById('modal-overlay')?.addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// ── STATUS BADGE HELPER ────────────────────────────────
function statusBadge(status) {
  const map = {
    'Active':       'badge-green',
    'Available':    'badge-green',
    'Scheduled':    'badge-blue',
    'In Progress':  'badge-amber',
    'Completed':    'badge-green',
    'Maintenance':  'badge-amber',
    'On Duty':      'badge-amber',
    'Cancelled':    'badge-red',
    'Retired':      'badge-grey',
    'Off Duty':     'badge-grey',
    'Linked':       'badge-blue',
    'Unlinked':     'badge-grey',
  };
  const cls = map[status] || 'badge-grey';
  return `<span class="badge ${cls}">${status}</span>`;
}

// ── CONFIRM DELETE ─────────────────────────────────────
function confirmDelete(message, onConfirm) {
  openModal('Confirm Delete', `
    <p style="color:var(--grey-100);margin-bottom:20px;">${message}</p>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="(${onConfirm.toString()})();closeModal()">Delete</button>
    </div>
  `);
}

// ── TABLE EMPTY STATE ──────────────────────────────────
function emptyState(message = 'No records found') {
  return `<tr><td colspan="99">
    <div class="empty-state">
      <div class="empty-state-icon">⬡</div>
      <div class="empty-state-text">${message}</div>
    </div>
  </td></tr>`;
}

// ── FORMAT DATE ────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}
