const demoItems = [
  { name: 'Passport', weight: 0.5, volume: 1.2, importance: 10 },
  { name: 'Toiletries kit', weight: 2.2, volume: 4.5, importance: 8 },
  { name: 'Hiking boots', weight: 1.8, volume: 3.1, importance: 9 },
  { name: 'Winter jacket', weight: 1.3, volume: 5.6, importance: 9 },
  { name: 'Laptop', weight: 2.4, volume: 6.0, importance: 10 },
  { name: 'Camera', weight: 1.1, volume: 2.4, importance: 7 },
  { name: 'Medications', weight: 0.7, volume: 1.5, importance: 10 },
  { name: 'Travel pillow', weight: 0.6, volume: 2.0, importance: 6 },
  { name: 'Socks & underwear', weight: 1.5, volume: 3.0, importance: 8 },
  { name: 'Power bank', weight: 0.9, volume: 2.3, importance: 7 }
];

const itemTable = document.getElementById('itemTable');
const solveBtn = document.getElementById('solveBtn');
const addItemButton = document.getElementById('addItem');
const loadDemoButton = document.getElementById('loadDemo');
const resetBtn = document.getElementById('resetBtn');

function createItemRow(item = { name: '', weight: '', volume: '', importance: '' }) {
  const row = document.createElement('div');
  row.className = 'item-row';
  row.innerHTML = `
    <input type="text" placeholder="Item name" value="${item.name || ''}" data-field="name" />
    <input type="number" min="0.1" step="0.1" placeholder="kg" value="${item.weight ?? ''}" data-field="weight" />
    <input type="number" min="0.1" step="0.1" placeholder="L" value="${item.volume ?? ''}" data-field="volume" />
    <input type="number" min="1" step="1" placeholder="score" value="${item.importance ?? ''}" data-field="importance" />
    <button type="button" class="remove-btn">Remove</button>
  `;

  row.querySelector('.remove-btn').addEventListener('click', () => row.remove());
  return row;
}

function renderItems(items) {
  itemTable.innerHTML = '';
  items.forEach(item => itemTable.appendChild(createItemRow(item)));
}

function getItemsFromForm() {
  const rows = [...itemTable.querySelectorAll('.item-row')];
  return rows.map(row => {
    const inputs = row.querySelectorAll('input');
    const values = Array.from(inputs).reduce((acc, input) => {
      acc[input.dataset.field] = input.value.trim();
      return acc;
    }, {});

    return {
      name: values.name || 'Unnamed item',
      weight: Number(values.weight || 0),
      volume: Number(values.volume || 0),
      importance: Number(values.importance || 0),
    };
  }).filter(item => item.name && item.weight > 0 && item.volume > 0 && item.importance > 0);
}

function updateSummary(data) {
  const dpImportance = document.getElementById('dpImportance');
  const greedyImportance = document.getElementById('greedyImportance');
  const usedWeight = document.getElementById('usedWeight');
  const usedVolume = document.getElementById('usedVolume');
  const dpItems = document.getElementById('dpItems');
  const greedyItems = document.getElementById('greedyItems');
  const analysisTable = document.getElementById('analysisTable');

  dpImportance.textContent = data.optimal.importance.toFixed(1);
  greedyImportance.textContent = data.greedy.importance.toFixed(1);
  usedWeight.textContent = `${data.optimal.weight.toFixed(1)} kg`;
  usedVolume.textContent = `${data.optimal.volume.toFixed(1)} L`;

  dpItems.innerHTML = data.optimal.selected.length
    ? data.optimal.selected.map(item => `<li>${item.name} (${item.weight.toFixed(1)} kg • ${item.volume.toFixed(1)} L • ${item.importance})</li>`).join('')
    : '<li>No items selected</li>';

  greedyItems.innerHTML = data.greedy.selected.length
    ? data.greedy.selected.map(item => `<li>${item.name} (${item.weight.toFixed(1)} kg • ${item.volume.toFixed(1)} L • ${item.importance})</li>`).join('')
    : '<li>No items selected</li>';

  analysisTable.innerHTML = data.analysis.length
    ? `
      <div class="analysis-row">
        <strong>Weight</strong>
        <strong>Volume</strong>
        <strong>Importance</strong>
        <strong>Selected items</strong>
      </div>
      ${data.analysis.map(item => `
        <div class="analysis-row">
          <span>${item.weight_capacity} kg</span>
          <span>${item.volume_capacity} L</span>
          <span>${item.importance.toFixed(1)}</span>
          <span>${item.selected.length ? item.selected.join(', ') : '—'}</span>
        </div>
      `).join('')}
    `
    : '<p>No analysis available</p>';
}

function solvePacking() {
  const items = getItemsFromForm();
  const weightCapacity = Number(document.getElementById('weightCapacity').value || 0);
  const volumeCapacity = Number(document.getElementById('volumeCapacity').value || 0);

  if (!items.length) {
    alert('Please add at least one valid item before solving the packing plan.');
    return;
  }

  if (!(weightCapacity > 0) || !(volumeCapacity > 0)) {
    alert('Please enter positive weight and volume limits.');
    return;
  }

  fetch('/api/pack', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items, weightCapacity, volumeCapacity })
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      updateSummary(data);
    })
    .catch(() => alert('Something went wrong while solving the packing plan.'));
}

function populateDemo() {
  document.getElementById('weightCapacity').value = 18;
  document.getElementById('volumeCapacity').value = 25;
  renderItems(demoItems);
  solvePacking();
}

addItemButton.addEventListener('click', () => {
  itemTable.appendChild(createItemRow());
});

solveBtn.addEventListener('click', solvePacking);
loadDemoButton.addEventListener('click', populateDemo);
resetBtn.addEventListener('click', populateDemo);

window.addEventListener('DOMContentLoaded', populateDemo);





























































































































































