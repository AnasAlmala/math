/* ================================================================
   GRE Quant Arabic Coach – Frontend Logic
================================================================ */

'use strict';

// ── DOM refs ──────────────────────────────────────────────────────
const loading       = document.getElementById('loading');
const questionCard  = document.getElementById('question-card');
const feedbackCard  = document.getElementById('feedback-card');

const qMeta         = document.getElementById('q-meta');
const qStem         = document.getElementById('q-stem');
const qcBlock       = document.getElementById('qc-block');
const qcCondition   = document.getElementById('qc-condition');
const colA          = document.getElementById('col-a');
const colB          = document.getElementById('col-b');
const answerSection = document.getElementById('answer-section');

const btnSubmit     = document.getElementById('btn-submit');
const btnNext       = document.getElementById('btn-next');

const feedbackHeader = document.getElementById('feedback-header');
const feedbackBody   = document.getElementById('feedback-body');

// Progress sidebar
const statAccuracy  = document.getElementById('stat-accuracy');
const statTotal     = document.getElementById('stat-total');
const statLevel     = document.getElementById('stat-level');
const areaBars      = document.getElementById('area-bars');

// ── State ─────────────────────────────────────────────────────────
let currentQuestion = null;
let startTime       = null;

// ── Area labels ──────────────────────────────────────────────────
const AREA_LABELS = {
  Arithmetic:   'الحساب',
  Algebra:      'الجبر',
  Geometry:     'الهندسة',
  DataAnalysis: 'تحليل البيانات',
};

const TYPE_LABELS = {
  QC: 'مقارنة كمية',
  MC: 'اختيار من متعدد',
  MA: 'اختيار متعدد',
  NE: 'إدخال رقمي',
};

// ── QC fixed choices ──────────────────────────────────────────────
const QC_CHOICES = [
  { key: 'A', label: 'الكمية في العمود (أ) أكبر' },
  { key: 'B', label: 'الكمية في العمود (ب) أكبر' },
  { key: 'C', label: 'الكميتان متساويتان'         },
  { key: 'D', label: 'لا يمكن تحديد العلاقة'      },
];

// ── Helpers ───────────────────────────────────────────────────────
function show(el)  { el.classList.remove('hidden'); }
function hide(el)  { el.classList.add('hidden'); }

function diffLabel(d) {
  return ['', 'سهل جداً', 'سهل', 'متوسط', 'صعب', 'صعب جداً'][d] || '';
}

// ── Load question ─────────────────────────────────────────────────
async function loadQuestion() {
  hide(questionCard);
  hide(feedbackCard);
  show(loading);

  try {
    const res = await fetch('/api/question');
    if (!res.ok) throw new Error('fetch failed');
    currentQuestion = await res.json();
    renderQuestion(currentQuestion);
    await loadProgress();
  } catch (e) {
    loading.innerHTML = '<p style="color:#dc2626">تعذّر تحميل السؤال. أعد تحميل الصفحة.</p>';
  }
}

// ── Render question ───────────────────────────────────────────────
function renderQuestion(q) {
  hide(loading);

  // Meta badges
  qMeta.innerHTML = `
    <span class="badge badge-area">${AREA_LABELS[q.content_area] || q.content_area}</span>
    <span class="badge badge-type">${TYPE_LABELS[q.question_type] || q.question_type}</span>
    <span class="badge badge-diff">${diffLabel(q.difficulty)}</span>
  `;

  // Stem
  qStem.textContent = q.stem_ar;

  // QC block
  if (q.question_type === 'QC') {
    show(qcBlock);
    qcCondition.textContent = q.condition_ar ? `الشرط: ${q.condition_ar}` : '';
    colA.textContent = q.col_a_ar || '';
    colB.textContent = q.col_b_ar || '';
  } else {
    hide(qcBlock);
  }

  // Answer section
  answerSection.innerHTML = buildAnswerSection(q);

  // Enable submit
  btnSubmit.disabled = false;

  show(questionCard);
  startTime = Date.now();
}

function buildAnswerSection(q) {
  if (q.question_type === 'QC') {
    const items = QC_CHOICES.map(c => `
      <label class="qc-choice">
        <input type="radio" name="qc_ans" value="${c.key}" />
        <span class="qc-key">${c.key}</span>
        <span>${c.label}</span>
      </label>
    `).join('');
    return `<span class="answer-label">اختر إجابتك:</span>
            <div class="qc-choices">${items}</div>`;
  }

  if (q.question_type === 'MC') {
    const items = (q.choices || []).map(ch => `
      <label class="choice-item">
        <input type="radio" name="mc_ans" value="${escHtml(ch)}" />
        <span>${escHtml(ch)}</span>
      </label>
    `).join('');
    return `<span class="answer-label">اختر الإجابة الصحيحة:</span>
            <div class="choices-list">${items}</div>`;
  }

  if (q.question_type === 'MA') {
    const items = (q.choices || []).map(ch => `
      <label class="choice-item">
        <input type="checkbox" name="ma_ans" value="${escHtml(ch)}" />
        <span>${escHtml(ch)}</span>
      </label>
    `).join('');
    return `<span class="answer-label">اختر كل الإجابات الصحيحة:</span>
            <div class="choices-list">${items}</div>`;
  }

  if (q.question_type === 'NE') {
    return `<span class="answer-label">أدخل إجابتك:</span>
            <input type="number" step="any" class="ne-input" id="ne-ans"
                   placeholder="أدخل الرقم" />`;
  }

  return '';
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Collect answer ────────────────────────────────────────────────
function collectAnswer(q) {
  if (q.question_type === 'QC') {
    const sel = document.querySelector('input[name="qc_ans"]:checked');
    return sel ? sel.value : null;
  }
  if (q.question_type === 'MC') {
    const sel = document.querySelector('input[name="mc_ans"]:checked');
    return sel ? sel.value : null;
  }
  if (q.question_type === 'MA') {
    const checked = [...document.querySelectorAll('input[name="ma_ans"]:checked')];
    return checked.length ? checked.map(c => c.value) : null;
  }
  if (q.question_type === 'NE') {
    const val = document.getElementById('ne-ans')?.value?.trim();
    return val !== '' ? val : null;
  }
  return null;
}

// ── Submit answer ─────────────────────────────────────────────────
btnSubmit.addEventListener('click', async () => {
  if (!currentQuestion) return;

  const answer = collectAnswer(currentQuestion);
  if (answer === null || answer === undefined ||
      (Array.isArray(answer) && answer.length === 0)) {
    showToast('اختر إجابة أولاً');
    return;
  }

  const timeTaken = Math.round((Date.now() - startTime) / 1000);
  btnSubmit.disabled = true;

  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question_id: currentQuestion.id,
        answer,
        time_taken: timeTaken,
      }),
    });

    const data = await res.json();
    renderFeedback(data);
    await loadProgress();
  } catch (e) {
    btnSubmit.disabled = false;
    showToast('حدث خطأ. حاول مرة أخرى.');
  }
});

// ── Render feedback ───────────────────────────────────────────────
function renderFeedback(data) {
  const ok = data.is_correct;

  feedbackCard.classList.remove('correct', 'wrong');
  feedbackCard.classList.add(ok ? 'correct' : 'wrong');

  feedbackHeader.className = 'feedback-header ' + (ok ? 'correct' : 'wrong');
  feedbackHeader.textContent = ok ? '✓ إجابة صحيحة!' : '✗ إجابة خاطئة';

  // Render feedback text with basic markdown-like bold (**text**)
  feedbackBody.innerHTML = mdBold(data.feedback || '');

  show(feedbackCard);
  feedbackCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function mdBold(text) {
  return escHtml(text).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

// ── Next question ─────────────────────────────────────────────────
btnNext.addEventListener('click', loadQuestion);

// ── Progress ──────────────────────────────────────────────────────
async function loadProgress() {
  try {
    const res = await fetch('/api/progress');
    const data = await res.json();
    renderProgress(data);
  } catch (_) { /* silent */ }
}

function renderProgress(data) {
  statAccuracy.textContent = data.total_attempts > 0
    ? data.accuracy + '%'
    : '—';
  statTotal.textContent  = data.total_attempts;
  statLevel.textContent  = data.thinking_level + ' / 4';

  // Area bars
  const byArea = data.by_area || {};
  const levels = data.content_levels || {};

  areaBars.innerHTML = Object.keys(AREA_LABELS).map(area => {
    const label = AREA_LABELS[area];
    const aData = byArea[area] || { total: 0, correct: 0 };
    const acc   = aData.total > 0
      ? Math.round(aData.correct / aData.total * 100)
      : null;
    const lvl   = levels[area] || 0;
    const pct   = Math.min(100, (lvl / 5) * 100);
    return `
      <div class="area-bar-row">
        <div class="area-bar-label">
          <span>${label}</span>
          <span>${acc !== null ? acc + '%' : '—'}</span>
        </div>
        <div class="area-bar-track">
          <div class="area-bar-fill" style="width:${pct}%"></div>
        </div>
      </div>
    `;
  }).join('');
}

// ── Toast ─────────────────────────────────────────────────────────
function showToast(msg) {
  const t = document.createElement('div');
  t.textContent = msg;
  Object.assign(t.style, {
    position: 'fixed', bottom: '1.5rem', left: '50%',
    transform: 'translateX(-50%)',
    background: '#1e293b', color: '#fff',
    padding: '.65rem 1.4rem', borderRadius: '8px',
    fontFamily: 'Cairo, sans-serif', fontSize: '.9rem',
    zIndex: 9999, opacity: '0', transition: 'opacity .2s',
  });
  document.body.appendChild(t);
  requestAnimationFrame(() => { t.style.opacity = '1'; });
  setTimeout(() => {
    t.style.opacity = '0';
    t.addEventListener('transitionend', () => t.remove());
  }, 2500);
}

// ── Boot ──────────────────────────────────────────────────────────
loadQuestion();
loadProgress();
