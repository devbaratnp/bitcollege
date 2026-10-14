"""Render the published BIT course structure without filling missing source data."""
from html import escape
from pathlib import Path
from urllib.parse import urlencode
import json

ROOT = Path(__file__).parent
DETAILS = {p['key']: p for p in json.loads((ROOT / 'content/program-details.json').read_text())['programs']}
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI']


def tabs(group, entries, name):
    links = ''.join(f'<a id="tab-{ident}" href="#{ident}" data-tab>{escape(title)}</a>' for ident, title, body in entries)
    panels = ''.join(f'<section id="{ident}" class="tab-panel" data-tab-panel><h3 class="tab-panel-title">{escape(title)}</h3>{body}</section>' for ident, title, body in entries)
    return f'<div class="content-tabs" data-tabs="{group}"><nav class="tab-list" aria-label="{escape(name)}">{links}</nav>{panels}</div>'


def render_program(p, programs, icon, photo, link, label):
    d = DETAILS[p['key']]
    esc = escape
    syllabus = d['official_curriculum']
    pdf = f'syllabus-{p["key"]}.pdf'
    local_pdf = (ROOT / 'dist/assets' / pdf).is_file()
    syllabus_url = '/assets/' + pdf if local_pdf else syllabus['url']
    syllabus_link = f'<a class="button button-outline-light" href="{syllabus_url}" download>Download Syllabus{icon("download")}</a>' if local_pdf else link(syllabus_url, 'Download Syllabus', 'button button-outline-light', external=True)
    apply_url = '/contact/?' + urlencode({'program': p['key'], 'subject': 'Admission inquiry'})
    overview = ''.join(f'<p>{esc(text)}</p>' for text in d['tabs']['overview'])
    eligibility = '''<p>All Nepalese and foreign candidates must meet CTEVT’s entrance requirements. Obtain the application form from BIT administration or an authorized centre, and pay the application fee set by CTEVT.</p>
        <ul class="clean-list"><li>General stream: SEE / SLC passed or equivalent.</li><li>The original BIT guide lists TSLC aggregate marks of 66.66% from IOE and 68.33% from CTEVT.</li><li>Foreign students: two copies of a domicile certificate or passport.</li></ul>
        <p class="course-note">These requirements are from BIT’s published course guide, dated 30 November 2022. Confirm the current intake criteria, entrance notice and documents with admissions before applying.</p>'''
    scope = '<p>Explore technical work and further study in these areas:</p><ul class="scope-list">' + ''.join(f'<li>{icon("check")}<span>{esc(text)}</span></li>' for text in d['tabs']['scope']) + '</ul>'
    overview_tabs = tabs('course-information', [('overview', 'Overview', overview), ('eligibility', 'Eligibility', eligibility), ('scope', 'Scope', scope)], 'Program information')
    other_programs = ''.join(f'<a href="/{q["slug"]}/">{esc(q["name"])}{icon("arrow-right")}</a>' for q in programs if q['key'] != p['key'])
    metadata = [('time', 'Duration', '3 years'), ('folder', 'Category', d['metadata']['category']), ('global', 'Language', d['metadata']['language']), ('graduation-cap', 'Affiliation', d['metadata']['affiliation'])]
    facts = ''.join(f'<div><dt>{icon(ico)}{title}</dt><dd>{esc(value)}</dd></div>' for ico, title, value in metadata)
    share_url = 'https://bit-campus.dkp1345ucc.chatgpt.site/' + p['slug'] + '/'
    email_url = 'mailto:?' + urlencode({'subject': d['title'], 'body': share_url})
    content = f'''<section class="section course-intro"><div class="container program-detail-grid"><article class="course-main">
        {photo(p['image'], p['name'] + ' practical learning at BIT', 'program-detail-photo', True)}
        <div class="course-heading">{label('ABOUT THE PROGRAM')}<h2>{esc(d['title'])}</h2><p class="course-updated">{icon('calendar-2')} Published course update: <time datetime="2022-11-30">30 Nov 2022</time></p></div>
        {overview_tabs}
        </article><aside class="program-sidebar"><div class="program-facts course-admission">{label('YOUR NEXT STEP')}<h2>GET ADMISSION</h2><p>Speak with BIT about this program and the current admission process.</p>{link(apply_url, 'Apply Now')}{syllabus_link}<dl>{facts}</dl><p class="syllabus-version">Official CTEVT curriculum · revised {syllabus['revision_year']}</p><a class="sidebar-text-link" href="/admission/">Admission process {icon('arrow-right')}</a></div>
        <div class="course-share"><h3>Share this course</h3><div class="share-buttons"><button class="icon-button" data-copy-course disabled aria-label="Copy course link">{icon('file-copy')}</button><a class="icon-button" href="{esc(email_url)}" aria-label="Share course by email">{icon('mail')}</a><button class="icon-button" data-native-share hidden aria-label="Share course">{icon('share')}</button></div><p data-share-status role="status"></p></div>
        <div class="sidebar-links"><h3>Explore other programs</h3>{other_programs}</div></aside></div></section>'''
    if d.get('youtube_embed_url'):
        content += f'''<section class="section course-video-section"><div class="container course-video-grid"><div>{label('EXPLORE THE FIELD')}<h2>COMPUTER ENGINEERING,<br>EXPLAINED.</h2><p>A 2021 guide to the CTEVT Computer Engineering diploma after SEE, linked from BIT’s course page.</p><p class="muted">Play to load the video from YouTube.</p></div><div class="course-video" data-video="7SHEdlpFhXk">{photo('computer-lab-group.jpg', 'Computer Engineering students in BIT’s laboratory')}<button data-load-video class="video-play" disabled>{icon('play-circle')}<span>Watch the course introduction</span></button><noscript><a class="video-fallback" href="https://www.youtube.com/watch?v=7SHEdlpFhXk" target="_blank" rel="noopener noreferrer">Watch on YouTube</a></noscript></div></div></section>'''
    benefits = ''.join(f'<li>{icon("checkbox-circle")}<span>{esc(text)}</span></li>' for text in d['why_choose']['benefits'])
    why_photo = f'program-{p["key"]}-why_choose.jpg'
    if not (ROOT / 'dist/assets' / why_photo).is_file():
        why_photo = p['image']
    why_alt = 'A technician working on an aircraft engine, featured in BIT’s Mechanical Engineering guide' if p['key'] == 'mechanical' else p['name'] + ' practical learning, featured by BIT'
    content += f'''<section class="section section-tint"><div class="container course-why-grid">{photo(why_photo, why_alt, 'course-why-photo')}<div>{label('WHY CHOOSE')}<h2>{esc(d['title']).upper()}?</h2><p>{esc(d['why_choose']['summary'])}</p><ul class="course-benefits">{benefits}</ul></div></div></section>'''
    semesters = []
    for semester in d['semesters']:
        number = semester['number']
        title = 'Semester ' + ROMAN[number - 1]
        rows = ''
        for index, subject in enumerate(semester['subjects'], 1):
            credit = esc(str(subject['credit_hours'])) if subject['credit_hours'] is not None else 'Not listed'
            marks = esc(str(subject['full_marks'])) if subject['full_marks'] is not None else 'Not listed'
            options = '<ul class="elective-options">' + ''.join(f'<li>{esc(option)}</li>' for option in subject['elective_options']) + '</ul>' if subject.get('elective_options') else ''
            rows += f'<tr><td>{index}</td><th scope="row">{esc(subject["subject"])}{options}</th><td>{credit}</td><td>{marks}</td></tr>'
        table = f'<div class="course-table-wrap" tabindex="0" role="region" aria-label="{title} subjects, scroll horizontally if needed"><table class="course-table"><caption>{esc(d["title"])} · {title}</caption><thead><tr><th scope="col">No.</th><th scope="col">Subjects</th><th scope="col">Credit hours</th><th scope="col">Full marks</th></tr></thead><tbody>{rows}</tbody></table></div>'
        semesters.append((f'semester-{number}', title, table))
    course_tabs = tabs('course-structure', semesters, 'Course semesters')
    content += f'''<section class="section course-structure"><div class="container"><div class="section-heading">{label(esc(d['title']).upper())}<h2>COURSE STRUCTURE</h2><p>Explore the subjects across all six semesters.</p></div>{course_tabs}<p class="course-note">BIT’s published tables do not provide subject codes, credit hours or full marks. Row numbers identify subjects only. Download the official CTEVT syllabus for the detailed curriculum and confirm the applicable revision with BIT.</p></div></section>'''
    outcomes = ''.join(f'<li>{icon("arrow-right")}<span>{esc(text)}</span></li>' for text in d['career_outcomes'])
    content += f'''<section class="section section-tint"><div class="container course-outcomes"><div>{label('AFTER YOUR DIPLOMA')}<h2>PUT YOUR<br>TECHNICAL SKILLS TO WORK.</h2><p>The published program guide highlights these areas for graduate skills and technical work.</p>{link('/contact/?program=' + p['key'], 'Discuss your next step', 'text-link')}</div><ul class="outcome-list">{outcomes}</ul></div></section>'''
    hod = d['hod']
    portrait = 'hod-computer.png' if p['key'] == 'computer' else f'hod-{p["key"]}.jpg'
    hod_image = photo(portrait, hod['name'], 'hod-portrait') if (ROOT / 'dist/assets' / portrait).is_file() else f'<span class="hod-symbol">{icon("user-star")}</span>'
    roster = ''.join(f'<li class="faculty-member"><span class="faculty-number">{index:02d}</span><div><h3>{esc(member["name"])}</h3><p>{esc(member["qualification"])}</p></div></li>' for index, member in enumerate(d['faculty'], 1))
    content += f'''<section class="section" id="faculty"><div class="container"><div class="department-heading"><div>{label('THE DEPARTMENT')}<h2>LEARN WITH<br>THE BIT TEAM.</h2></div><div class="hod-card">{hod_image}<div><h3>{esc(hod['name'])}</h3><p>{esc(hod['role_source'])}</p></div></div></div><h2 class="faculty-title">Faculty Members</h2><ul class="faculty-list">{roster}</ul><p class="course-note">Faculty names, qualifications and department roles follow BIT’s published course page. Contact the institute for the current teaching team.</p><div class="course-source">{link(d['source_url'], 'Original BIT program page', 'text-link', external=True)}{link(syllabus_url, 'Official CTEVT syllabus', 'text-link', external=not local_pdf)}</div></div></section>'''
    return content
