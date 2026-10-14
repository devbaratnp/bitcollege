# Verification matrix

| Area | Evidence | Result |
|---|---|---|
| Page routes, assets, fonts, icons | validate_site.py, 39 HTML files including 404 copy | Passed |
| Metadata, headings, IDs, dialog names | Static validation | Passed |
| JavaScript syntax | node --check dist/app.js | Passed |
| Notice search/year/category/reset | jsdom interaction suite | Passed |
| Navigation state and Escape focus logic | jsdom interaction suite | Passed |
| Gallery filtering and image captions | jsdom interaction suite | Passed |
| Inquiry validation, no-JS fallback, plain-text draft | jsdom interaction suite | Passed |
| Five courses, 30 semesters and elective choices | Compared rendered tables with researched data | Passed |
| Full faculty rosters | 58 rendered names/qualifications across five programs | Passed |
| Syllabus downloads | All five local files start with PDF signature | Passed |
| Course information/semester keyboard tabs | Click, Home/End, arrow wrap, selected state, hash links, no-JS visibility | Passed |
| Expanded homepage support tabs and sections | jsdom interaction suite | Passed |
| Copy/share/email controls and delayed video | jsdom interaction suite, honest clipboard fallback | Passed |
| Desktop/mobile layout, visual fidelity | Supervised preview unavailable | Blocked |
| Native dialog focus and browser console | No rendered browser session | Unverified |
| Official syllabus PDFs and two HOD portraits | Successful official byte downloads; new imagery inspected | Passed |
| Older notice archive documents | Earlier source download attempts failed | Availability unverified |
