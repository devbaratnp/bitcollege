(() => {
  'use strict';
  const all = (selector, root = document) => [...root.querySelectorAll(selector)];
  const one = (selector) => document.querySelector(selector);
  const groups = all('.nav-group');
  const closeNav = () => groups.forEach(group => {
    group.classList.remove('open');
    group.querySelector('.nav-trigger').setAttribute('aria-expanded', 'false');
  });
  groups.forEach(group => {
    const trigger = group.querySelector('.nav-trigger');
    trigger.addEventListener('click', () => {
      const open = group.classList.contains('open');
      closeNav();
      if (!open) { group.classList.add('open'); trigger.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', event => { if (!event.target.closest('.nav-group')) closeNav(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      const open = one('.nav-group.open');
      closeNav();
      if (open) open.querySelector('.nav-trigger').focus();
    }
  });
  const openDialog = dialog => { dialog.showModal(); document.body.classList.add('dialog-open'); };
  all('dialog').forEach(dialog => {
    dialog.addEventListener('close', () => { if (!one('dialog[open]')) document.body.classList.remove('dialog-open'); });
    dialog.addEventListener('click', event => { if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }});
  });
  all('[data-close-dialog]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
  const menu = one('#mobile-menu');
  one('[data-open-menu]')?.addEventListener('click', () => openDialog(menu));

  const lightbox = one('#photo-lightbox');
  all('[data-lightbox]').forEach(button => button.addEventListener('click', () => {
    const img = lightbox.querySelector('img');
    img.src = button.dataset.lightbox;
    img.alt = button.dataset.caption;
    lightbox.querySelector('p').textContent = button.dataset.caption;
    openDialog(lightbox);
  }));
  all('[data-gallery-filter]').forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.galleryFilter;
    all('[data-gallery-filter]').forEach(tab => {
      const selected = tab === button;
      tab.classList.toggle('active', selected);
      tab.setAttribute('aria-pressed', String(selected));
    });
    all('[data-gallery-category]').forEach(item => { item.hidden = category !== 'all' && item.dataset.galleryCategory !== category; });
  }));

  const query = one('#notice-query');
  if (query) {
    const year = one('#notice-year'), category = one('#notice-category'), rows = all('[data-notice]');
    const filter = () => {
      const search = query.value.trim().toLocaleLowerCase();
      let count = 0;
      rows.forEach(row => {
        const visible = row.dataset.search.includes(search) && (year.value === 'all' || row.dataset.year === year.value) && (category.value === 'all' || row.dataset.category === category.value);
        row.hidden = !visible;
        if (visible) count++;
      });
      one('#notice-count').textContent = `${count} ${count === 1 ? 'notice' : 'notices'}`;
      one('#notice-empty').hidden = count !== 0;
    };
    query.addEventListener('input', filter);
    year.addEventListener('change', filter);
    category.addEventListener('change', filter);
    one('#notice-search').addEventListener('submit', event => { event.preventDefault(); filter(); });
    one('#reset-notices').addEventListener('click', () => { query.value = ''; year.value = 'all'; category.value = 'all'; filter(); query.focus(); });
  }

  const enquiry = one('#enquiry-form');
  if (enquiry) {
    const params = new URLSearchParams(location.search);
    const selected = params.get('program');
    if (selected && [...enquiry.elements.program.options].some(option => option.value === selected)) enquiry.elements.program.value = selected;
    const subject = (params.get('subject') || 'BIT inquiry').slice(0, 120);
    enquiry.addEventListener('submit', event => {
      event.preventDefault();
      if (!enquiry.reportValidity()) return;
      const data = new FormData(enquiry);
      const program = enquiry.elements.program.selectedOptions[0].textContent;
      const body = `Hello BIT,\n\n${String(data.get('message')).trim()}\n\nName: ${String(data.get('name')).trim()}\nEmail: ${String(data.get('email')).trim()}\nPhone: ${String(data.get('phone')).trim() || 'Not provided'}\nProgram: ${program}`;
      one('#email-body').textContent = body;
      one('#open-email').href = `mailto:info.bitcollege@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      openDialog(one('#email-preview'));
    });
    one('#review-inquiry').disabled = false;
  }

  // With JavaScript disabled, every section remains visible and the links are anchors.
  all('[data-tabs]').forEach(group => {
    const tabs = all('[data-tab]', group);
    const panels = all('[data-tab-panel]', group);
    const select = (index, focus = false, updateHash = false) => {
      tabs.forEach((tab, i) => {
        const selected = i === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[i].hidden = !selected;
      });
      if (focus) tabs[index].focus();
      if (updateHash) history.replaceState(null, '', tabs[index].getAttribute('href'));
    };
    group.querySelector('.tab-list').setAttribute('role', 'tablist');
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', event => { event.preventDefault(); select(index, false, true); });
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next, true, true); }
      });
    });
    const selectHash = () => {
      const found = tabs.findIndex(tab => tab.getAttribute('href') === location.hash);
      if (found !== -1) select(found);
      return found;
    };
    if (selectHash() === -1) select(0);
    window.addEventListener('hashchange', selectHash);
    group.classList.add('tabs-ready');
  });

  const copyCourse = one('[data-copy-course]');
  if (copyCourse) {
    const courseUrl = one('link[rel="canonical"]').href;
    const status = one('[data-share-status]');
    copyCourse.addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(courseUrl);
        status.textContent = 'Course link copied.';
      } catch { status.textContent = `Copy this link: ${courseUrl}`; }
    });
    copyCourse.disabled = false;
    const share = one('[data-native-share]');
    if (navigator.share) {
      share.hidden = false;
      share.addEventListener('click', async () => {
        try { await navigator.share({ title: document.title, url: courseUrl }); }
        catch (error) { if (error.name !== 'AbortError') status.textContent = `Share this link: ${courseUrl}`; }
      });
    }
  }

  all('[data-load-video]').forEach(button => {
    const container = button.closest('[data-video]');
    if (!/^[A-Za-z0-9_-]{11}$/.test(container.dataset.video)) return;
    button.addEventListener('click', () => {
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${container.dataset.video}?autoplay=1`;
      frame.title = 'Diploma in Computer Engineering in Nepal: CTEVT course introduction';
      frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      container.replaceChildren(frame);
    }, { once: true });
    button.disabled = false;
  });

  const topButton = one('[data-back-top]');
  const updateTop = () => {
    const visible = scrollY > 700;
    topButton.classList.toggle('visible', visible);
    topButton.hidden = !visible;
  };
  window.addEventListener('scroll', updateTop, { passive: true });
  updateTop();
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'auto' : 'smooth' }));
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion:reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('reveal'); observer.unobserve(entry.target); }
    }), { threshold: .08 });
    all('.section-heading,.about-copy,.program-card,.facility-card').forEach(element => observer.observe(element));
  }
})();
