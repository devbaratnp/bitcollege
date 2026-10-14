# BIT campus redesign

Approved visual: the second homepage concept, Campus / Institutional Confidence. A static multi-page redesign using BIT’s original logo and authentic campus/student photographs.

## Local source

- `build_site.py` generates the public pages in `dist/`.
- `home_sections.py` renders the expanded support, leadership, alumni and campus sections.
- `course_pages.py` renders the shared detailed program format from `content/program-details.json`.
- `dist/styles.css` contains the shared responsive design.
- `dist/app.js` implements menus, archive filtering, lightboxes and email-draft review.
- `docs/CONTENT_SOURCES.md` records verified source content and unresolved institution details.
- `docs/reference/campus-concept.png` preserves the approved design target.

Run `python3 build_site.py` to regenerate HTML, `npm run check` for source checks, and `npm install --ignore-scripts && npm test` for DOM interaction tests. The published static files need no runtime Node/Python dependency.

## Visitor flows

Navigation resolves to static pages. The homepage includes reasons to choose BIT, student support tabs, the principal’s welcome, academic departments, five published alumni profiles, campus stories and summarized student feedback. All five program pages include overview/eligibility/scope tabs, admission details, official syllabus PDFs, reasons to choose the field, six semester tables with elective choices, career directions and full published faculty lists. Course tabs support keyboard navigation and linked sections; all content remains visible without JavaScript. Course sharing has clipboard, email and supported native-share options. The Computer page loads its source-linked explainer video only after a visitor clicks play.

The notice archive contains ten historical records with original dates. Campus photos can be filtered and opened in an accessible native dialog. Contact forms prepare a plain-text email draft for review and the visitor’s own email app; no server sends or stores inquiries.

## Current release state

Public review Site, as requested by the owner: https://bit-campus.dkp1345ucc.chatgpt.site. Search indexing remains intentionally disabled. The college’s original live domain was not modified. Course information retains its source update date, 30 November 2022. Historical eligibility is labeled accordingly; current fees, admission dates and scholarship availability require the current BIT/CTEVT notice.

Internal link, asset, heading, icon, dialog-label and font checks pass. Seven DOM interaction suites pass, including all 30 semester tables, 58 faculty records, keyboard tabs, syllabus signatures, sharing and video activation. Browser visual/responsive verification remains unavailable in the managed environment. Native rendering and modal focus behavior remain to be checked before an official college-domain release.
