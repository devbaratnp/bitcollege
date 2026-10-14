const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const { JSDOM } = require(require.resolve('jsdom', { paths: [process.env.BIT_QA_NODE_MODULES || root] }));
const script = fs.readFileSync(path.join(root, 'dist/app.js'), 'utf8');
const passed = [];

function page(route, search = '', start = true) {
  const file = path.join(root, 'dist', route, 'index.html');
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { url: `https://bit.test/${route ? route + '/' : ''}${search}`, runScripts: 'outside-only' });
  const w = dom.window;
  w.matchMedia = () => ({ matches: true });
  w.scrollTo = () => {};
  // jsdom has no native dialog UI. Model its open/close events for logic tests only.
  w.HTMLDialogElement.prototype.showModal = function () { this.setAttribute('open', ''); };
  w.HTMLDialogElement.prototype.close = function () { this.removeAttribute('open'); this.dispatchEvent(new w.Event('close')); };
  if (start) w.eval(script);
  return { dom, w, d: w.document, start: () => w.eval(script) };
}

{
  const { dom, w, d } = page('notices');
  const visible = () => [...d.querySelectorAll('[data-notice]')].filter(n => !n.hidden);
  assert.equal(visible().length, 10);
  const query = d.querySelector('#notice-query');
  query.value = 'nonexistent-keyword'; query.dispatchEvent(new w.Event('input'));
  assert.equal(visible().length, 0); assert.equal(d.querySelector('#notice-empty').hidden, false);
  d.querySelector('#reset-notices').click(); assert.equal(visible().length, 10);
  const year = d.querySelector('#notice-year'); year.value = '2024'; year.dispatchEvent(new w.Event('change'));
  assert.equal(visible().length, 1); assert.match(visible()[0].textContent, /examination centre details/);
  const category = d.querySelector('#notice-category'); category.value = 'Admissions'; category.dispatchEvent(new w.Event('change'));
  assert.equal(visible().length, 0);
  year.value = 'all'; year.dispatchEvent(new w.Event('change')); assert.equal(visible().length, 3);
  passed.push('Ten-notice archive, combined year/category/search filters, empty state and reset'); dom.window.close();
}
{
  const { dom, w, d } = page('');
  const trigger = d.querySelector('[aria-controls="program-menu"]');
  trigger.click(); assert.equal(trigger.getAttribute('aria-expanded'), 'true');
  d.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  assert.equal(trigger.getAttribute('aria-expanded'), 'false'); assert.equal(d.activeElement, trigger);
  d.querySelector('[data-open-menu]').click(); assert.equal(d.querySelector('#mobile-menu').open, true);
  assert.equal(d.body.classList.contains('dialog-open'), true);
  d.querySelector('#mobile-menu [data-close-dialog]').click(); assert.equal(d.querySelector('#mobile-menu').open, false);
  assert.equal(d.body.classList.contains('dialog-open'), false);
  assert.equal(d.querySelector('[data-back-top]').hidden, true);
  passed.push('Navigation toggle, Escape focus return, menu open/close logic and hidden top control'); dom.window.close();
}
{
  const { dom, d } = page('campus-life');
  d.querySelector('[data-gallery-filter="community"]').click();
  const visible = [...d.querySelectorAll('[data-gallery-category]')].filter(n => !n.hidden);
  assert.equal(visible.length, 5);
  visible[0].click(); assert.equal(d.querySelector('#photo-lightbox').open, true);
  assert.equal(d.querySelector('#photo-lightbox img').alt, visible[0].dataset.caption);
  assert.match(d.querySelector('#photo-lightbox img').src, /industrial-visit/);
  d.querySelector('#photo-lightbox [data-close-dialog]').click(); assert.equal(d.querySelector('#photo-lightbox').open, false);
  passed.push('Gallery category filtering, caption-safe image lightbox and close flow'); dom.window.close();
}
{
  const { dom, w, d, start } = page('contact', '?program=computer&subject=Admission%20inquiry', false);
  assert.equal(d.querySelector('#review-inquiry').disabled, true, 'No-JS form must not submit personal information in a GET URL');
  start(); assert.equal(d.querySelector('#review-inquiry').disabled, false);
  const form = d.querySelector('#enquiry-form'); assert.equal(form.elements.program.value, 'computer');
  form.dispatchEvent(new w.Event('submit', { cancelable: true })); assert.equal(d.querySelector('#email-preview').open, false);
  form.elements.name.value = 'Test Student'; form.elements.email.value = 'student@example.com'; form.elements.phone.value = '9800000000';
  form.elements.message.value = '<img src=x onerror=alert(1)> Please share admission details.';
  form.dispatchEvent(new w.Event('submit', { cancelable: true }));
  assert.equal(d.querySelector('#email-preview').open, true);
  assert.equal(d.querySelector('#email-body img'), null, 'Message must remain plain text');
  assert.match(d.querySelector('#email-body').textContent, /<img src=x onerror=alert\(1\)>/);
  const email = new URL(d.querySelector('#open-email').href);
  assert.equal(email.protocol, 'mailto:'); assert.equal(email.pathname, 'info.bitcollege@gmail.com');
  assert.equal(email.searchParams.get('subject'), 'Admission inquiry'); assert.match(email.searchParams.get('body'), /Program: Computer Engineering/);
  assert.equal(w.location.search, '?program=computer&subject=Admission%20inquiry');
  passed.push('Safe no-JS fallback, required input validation, preselected program and escaped reviewable email draft'); dom.window.close();
}
async function courseChecks() {
  const settle = () => new Promise(resolve => setImmediate(resolve));
  const details = JSON.parse(fs.readFileSync(path.join(root, 'content/program-details.json'), 'utf8')).programs;
  for (const course of details) {
    const { dom, w, d, start } = page(course.slug, '#semester-6', false);
    const panels = [...d.querySelectorAll('[data-tab-panel]')];
    assert.equal(panels.length, 9);
    assert(panels.every(panel => !panel.hidden), 'All content must remain available without JavaScript');
    assert.equal(d.querySelector('[data-copy-course]').disabled, true);
    assert.equal(d.querySelectorAll('.faculty-member').length, course.faculty.length);
    assert(d.querySelector('#faculty'));
    const download = d.querySelector('.course-admission a[download]');
    const pdf = fs.readFileSync(path.join(root, 'dist', download.getAttribute('href')));
    assert.equal(pdf.subarray(0, 4).toString(), '%PDF');
    course.semesters.forEach(semester => {
      const panel = d.querySelector(`#semester-${semester.number}`);
      assert.equal(panel.querySelectorAll('tbody tr').length, semester.subjects.length);
      assert(panel.textContent.includes('Not listed'));
      for (const subject of semester.subjects) {
        assert(panel.textContent.includes(subject.subject));
        for (const option of subject.elective_options || []) assert(panel.textContent.includes(option));
      }
    });
    start();
    assert.equal(d.querySelector('#semester-6').hidden, false, 'Semester deep links must open the requested tab');
    assert.equal(d.querySelector('#semester-1').hidden, true);
    const info = d.querySelector('[data-tabs="course-information"]');
    const tab = info.querySelector('[href="#eligibility"]');
    tab.click(); assert.equal(d.querySelector('#eligibility').hidden, false);
    assert.equal(d.querySelector('#overview').hidden, true);
    assert.equal(tab.getAttribute('aria-selected'), 'true');
    tab.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'End', bubbles: true, cancelable: true }));
    assert.equal(d.activeElement.id, 'tab-scope'); assert.equal(d.querySelector('#scope').hidden, false);
    d.activeElement.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true, cancelable: true }));
    assert.equal(d.activeElement.id, 'tab-overview');
    d.activeElement.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowLeft', bubbles: true, cancelable: true }));
    assert.equal(d.activeElement.id, 'tab-scope');
    d.activeElement.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Home', bubbles: true, cancelable: true }));
    assert.equal(d.activeElement.id, 'tab-overview');
    for (const group of d.querySelectorAll('[data-tabs]')) {
      assert.equal(group.querySelectorAll('[aria-selected="true"]').length, 1);
      assert.equal([...group.querySelectorAll('[data-tab-panel]')].filter(panel => !panel.hidden).length, 1);
    }
    dom.window.close();
  }
  passed.push('Five courses: all six semester datasets, 58 faculty entries, real PDF downloads, no-JS content, deep links and keyboard tabs');
  {
    const { dom, d } = page('');
    d.querySelector('[href="#support-scholarships"]').click();
    assert.equal(d.querySelector('#support-scholarships').hidden, false);
    assert.equal(d.querySelector('#support-library').hidden, true);
    assert.equal(d.querySelectorAll('.home-department').length, 5);
    assert.equal(d.querySelectorAll('.alumni-pathway').length, 5);
    assert.equal(d.querySelectorAll('.campus-story').length, 3);
    passed.push('Expanded homepage: student-support tabs, five department links, alumni pathways and campus stories');
    dom.window.close();
  }
  {
    const { dom, w, d, start } = page('diploma-in-computer-engineering', '', false);
    let copied, shared;
    Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: async url => { copied = url; } }, configurable: true });
    w.navigator.share = async data => { shared = data; };
    start();
    d.querySelector('[data-copy-course]').click(); await settle();
    assert.equal(copied, d.querySelector('link[rel="canonical"]').href);
    assert.equal(d.querySelector('[data-share-status]').textContent, 'Course link copied.');
    delete w.navigator.clipboard;
    d.querySelector('[data-copy-course]').click(); await settle();
    assert.match(d.querySelector('[data-share-status]').textContent, /^Copy this link: https:/);
    assert.equal(d.querySelector('[data-native-share]').hidden, false);
    d.querySelector('[data-native-share]').click(); await settle();
    assert.equal(shared.url, copied);
    const email = new URL(d.querySelector('.share-buttons a').href);
    assert.equal(email.protocol, 'mailto:'); assert.equal(email.searchParams.get('body'), copied);
    assert.equal(d.querySelector('.course-video iframe'), null, 'YouTube must load only when requested');
    d.querySelector('[data-load-video]').click();
    assert.match(d.querySelector('.course-video iframe').src, /^https:\/\/www.youtube-nocookie.com\/embed\/7SHEdlpFhXk\?autoplay=1$/);
    assert(d.querySelector('.course-video iframe').title);
    passed.push('Course sharing: clipboard success/fallback, native share and email URL; video loads only after a click');
    dom.window.close();
  }
  console.log(JSON.stringify({ passed: passed.length, tests: passed, environment: 'jsdom DOM logic tests; not browser rendering or native modal UI verification' }, null, 2));
}
courseChecks().catch(error => { console.error(error); process.exitCode = 1; });
