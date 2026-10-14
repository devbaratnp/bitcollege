# Design QA

Source visual truth: docs/reference/campus-concept.png (second displayed generated concept).
Target: campus-led BIT homepage, 1440px logical desktop frame; responsive mobile adaptation.
State: homepage and supporting visitor workflows.

Implementation screenshot: unavailable.
Viewport / pixel-density normalization: not available; no successful browser capture.
Full-view and focused comparison evidence: blocked.

The supervised preview command exits before serving with `bwrap: Can't mount proc on /newroot/proc: Operation not permitted`. Status reports stopped. The application was not changed to replace or bypass managed preview infrastructure.

Source checks passed: internal links/assets, unique IDs, one H1/title, named dialogs, valid icon glyphs, locally available fonts and noindex metadata. Seven jsdom DOM-logic suites passed for existing visitor flows, all five expanded courses, homepage support tabs, PDF downloads, course sharing and delayed video loading. These are not browser rendering or native modal interaction evidence.

Expansion retains the approved campus direction, institutional blue/yellow colors, real campus photography and heading/body fonts. New course tables scroll inside a labeled wrapper on narrow screens; tab bars have horizontal overflow and keyboard support. These responsive rules have been inspected in source but not rendered in a browser. New BIT portraits and program imagery were visually inspected separately from layout QA.

Fixed in source review: replaced chemistry image on Electrical & Electronics, restored two omitted archived notices, added dialog accessible names, made contact submission inert before JavaScript initializes, hid the inactive back-to-top control from focus.

Remaining required verification: desktop visual comparison with the approved target, 390px/768px mobile layout and overflow checks, keyboard focus trapping/return, loaded fonts/photos, browser console and actual core visitor flows.

final result: blocked
