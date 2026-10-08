* {
  box-sizing: border-box;
}

:root {
  --bg: #f4f7fb;
  --panel: #ffffff;
  --panel-alt: #eef5ff;
  --border: #dfe8f5;
  --primary: #1d4ed8;
  --primary-soft: rgba(29, 78, 216, 0.12);
  --secondary: #0f172a;
  --success: #0f766e;
  --warning: #f59e0b;
  --danger: #dc2626;
  --muted: #64748b;
  --text: #111827;
  --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg, #ecf2ff 0%, #f8fafc 100%);
  color: var(--text);
}

button,
input {
  font: inherit;
}

.page-shell {
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 26px;
}

.eyebrow {
  margin: 0 0 8px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--primary);
  font-size: 0.72rem;
  font-weight: 700;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 0;
  font-size: clamp(2rem, 2.8vw, 3rem);
}

.layout {
  display: grid;
  grid-template-columns: minmax(340px, 1fr) minmax(380px, 1.15fr);
  gap: 26px;
}

.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 24px;
  box-shadow: var(--shadow);
  padding: 24px;
}

.panel-header,
.section-header,
.analysis-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(160px, 1fr));
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.88rem;
  color: var(--muted);
  font-weight: 600;
}

input {
  width: 100%;
  border: 1px solid var(--border);
  background: #f8fbff;
  border-radius: 12px;
  padding: 12px 14px;
  color: var(--text);
}

input:focus {
  outline: 2px solid rgba(29, 78, 216, 0.15);
  border-color: rgba(29, 78, 216, 0.55);
}

.section-header {
  margin-top: 26px;
  margin-bottom: 14px;
}

.item-table {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item-row {
  display: grid;
  grid-template-columns: 1.4fr 0.9fr 0.9fr 0.9fr auto;
  gap: 10px;
  align-items: center;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px;
}

.item-row .remove-btn {
  background: rgba(220, 38, 38, 0.08);
  color: var(--danger);
  border: none;
  border-radius: 10px;
  padding: 10px 12px;
  font-weight: 700;
  cursor: pointer;
}

.primary-button,
.secondary-button,
.ghost-button {
  border: none;
  border-radius: 12px;
  padding: 12px 18px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.primary-button {
  background: linear-gradient(135deg, var(--primary), #3b82f6);
  color: white;
  box-shadow: 0 12px 28px rgba(29, 78, 216, 0.2);
}

.secondary-button {
  background: var(--primary-soft);
  color: var(--primary);
}

.secondary-button.small {
  padding: 9px 12px;
  font-size: 0.8rem;
}

.ghost-button {
  background: #edf2f7;
  color: var(--secondary);
}

.primary-button:hover,
.secondary-button:hover,
.ghost-button:hover,
.item-row .remove-btn:hover {
  transform: translateY(-1px);
}

.actions-row {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(150px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.metric-card {
  background: linear-gradient(180deg, #f8fbff, #eff6ff);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 18px 16px;
}

.metric-card.accent {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.1), rgba(59, 130, 246, 0.15));
}

.label,
.mini-label {
  display: block;
  color: var(--muted);
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
}

.metric-card strong {
  display: block;
  font-size: clamp(1.4rem, 2vw, 2rem);
  margin-top: 10px;
}

.result-comparison {
  display: grid;
  grid-template-columns: repeat(2, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-list li {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 12px;
  background: #f8fafc;
}

.analysis-box {
  border: 1px solid var(--border);
  border-radius: 18px;
  background: linear-gradient(180deg, #fcfdff, #f6f9ff);
  padding: 18px 14px;
}

.analysis-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.analysis-row {
  display: grid;
  grid-template-columns: 1.1fr 1.1fr 1.2fr 2fr;
  gap: 8px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: white;
  font-size: 0.88rem;
}

@media (max-width: 920px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  .item-row {
    grid-template-columns: 1fr 1fr;
  }
  .field-grid,
  .metric-grid,
  .result-comparison {
    grid-template-columns: 1fr;
  }
  .topbar,
  .actions-row,
  .panel-header,
  .section-header,
  .analysis-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
