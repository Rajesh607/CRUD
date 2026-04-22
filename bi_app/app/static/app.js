const token = localStorage.getItem('token');
const output = document.getElementById('output');
if (!token) window.location = '/';

function authHeaders(extra = {}) {
  return { Authorization: `Bearer ${token}`, ...extra };
}

function show(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

async function submitUpload(e, companyType) {
  e.preventDefault();
  const formData = new FormData(e.target);
  formData.append('company_type', companyType);
  const res = await fetch('/api/v1/upload', {
    method: 'POST',
    headers: authHeaders(),
    body: formData,
  });
  output.textContent = JSON.stringify(await res.json(), null, 2);
}

async function loadHistory() {
  const res = await fetch('/api/v1/uploads', { headers: authHeaders() });
  output.textContent = JSON.stringify(await res.json(), null, 2);
}

document.getElementById('analyzeForm').onsubmit = async (e) => {
  e.preventDefault();
  const body = Object.fromEntries(new FormData(e.target).entries());
  body.company_a_id = Number(body.company_a_id);
  body.target_company_id = Number(body.target_company_id);
  const res = await fetch('/api/v1/analyze', {
    method: 'POST',
    headers: authHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  });
  output.textContent = JSON.stringify(await res.json(), null, 2);
};
