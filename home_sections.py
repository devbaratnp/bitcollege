"""Expanded homepage sections drawn from BIT's published institution content."""

from html import escape
from pathlib import Path
from course_pages import tabs

ROOT = Path(__file__).parent
HOD_PHOTOS = {'computer': 'staff-sarita.jpg', 'civil': 'staff-sudhir.jpg', 'electrical-electronics': 'staff-simran.jpg', 'mechanical': 'staff-jay.jpg'}


def home_expansion(programs, details, icon, photo, link, label):
    reasons = [
        ('graduation-cap', 'CTEVT affiliated', 'Five diploma pathways within Nepal’s technical and vocational education system.'),
        ('tools', 'Learn through practice', 'Laboratory sessions, workshops and field activities connect theory with technical work.'),
        ('group', 'Tutorial support', 'Small-group tutorial classes help students work through classroom concepts.'),
        ('book-open', 'Resources for study', 'Computer labs, a library and a study room support learning beyond scheduled classes.'),
        ('medal', 'Scholarship guidance', 'Explore CTEVT schemes and BIT’s published merit-based scholarship information.'),
        ('parent', 'A connected learning community', 'BIT’s published approach includes sharing student progress with parents.'),
    ]
    cards = ''.join(f'<article class="why-bit-item"><span>{icon(ico)}</span><h3>{title}</h3><p>{text}</p></article>' for ico, title, text in reasons)
    html = f'''<section class="section why-bit"><div class="container"><div class="section-heading">{label('04 / WHY BIT')}<div><h2>THE SUPPORT TO LEARN.<br>THE SPACE TO GROW.</h2><p class="heading-copy">A technical education shaped by practical experience, academic support and campus life.</p></div></div><div class="why-bit-grid">{cards}</div></div></section>'''
    support = [
        ('support-library', 'Library & resources', f'<div class="support-panel">{photo("library-students.jpg", "BIT students studying in the college library")}<div><h3>A place for focused study.</h3><p>BIT describes a furnished library with textbooks, journals and a study room. Semester learning resources help students continue their work outside the classroom.</p>{link("/campus-life/", "Explore campus facilities", "text-link")}</div></div>'),
        ('support-scholarships', 'Scholarships', f'<div class="support-panel">{photo("computer-lab.jpg", "A BIT student working in the computer laboratory")}<div><h3>Understand your options.</h3><p>BIT publishes information on CTEVT classified and special scholarship schemes, alongside internal merit-based support linked to semester results.</p><p>Ask the admissions office about current availability, eligibility and the application process.</p>{link("/scholarship/", "Scholarship information", "text-link")}</div></div>'),
        ('support-teaching', 'Teaching & guidance', f'<div class="support-panel">{photo("electronics-practical.jpg", "BIT students receiving guidance during electronics practical work")}<div><h3>Learning with technical guidance.</h3><p>Explore the published faculty team across Computer, Civil, Electrical, Electrical & Electronics, and Mechanical Engineering. Classroom teaching is supported by practical sessions and tutorial learning.</p>{link("/management-team/", "Meet our people", "text-link")}</div></div>'),
    ]
    # Panel body includes its own descriptive heading; the tab label remains the accessible panel heading.
    html += f'''<section class="section section-tint student-support"><div class="container"><div class="section-heading">{label('05 / STUDENT SUPPORT')}<h2>MORE THAN A CLASSROOM.</h2></div>{tabs('student-support', support, 'Student support')}</div></section>'''
    html += f'''<section class="section principal-home"><div class="container principal-home-grid"><div class="principal-campus">{photo('campus.webp', 'BIT’s campus courtyard and academic building')}<div>{icon('graduation-cap')}<span>Technical education<br>with a practical purpose.</span></div></div><div>{label('A MESSAGE FROM THE PRINCIPAL')}<h2>WELCOME TO<br>YOUR NEXT CHAPTER.</h2><p>BIT’s principal welcomes students to an institute focused on technical knowledge and practical skills. Explore the five diploma programs and the learning community that supports them.</p><div class="principal-signature"><h3>Er. Niraj Shriwastav</h3><span>Principal, Birgunj Institute of Technology</span></div>{link('/principal-message/', 'Read the principal’s message', 'text-link')}</div></div></section>'''
    team = ''
    for p in programs:
        hod = details[p['key']]['hod']
        hod_photo = HOD_PHOTOS.get(p['key'], '')
        if hod_photo and (ROOT / 'dist' / 'assets' / hod_photo).is_file():
            visual = photo(hod_photo, hod['name'], 'department-photo')
        else:
            visual = f'<span class="department-icon">{icon(p["icon"])}</span>'
        team += f'<a class="home-department" href="/{p["slug"]}/#faculty">{visual}<span class="department-subject">{escape(p["name"])}</span><h3>{escape(hod["name"])}</h3><span class="department-role">{escape(hod["role_source"])}</span><span class="department-link">Meet the faculty {icon("arrow-right")}</span></a>'
    html += f'''<section class="section section-tint"><div class="container"><div class="section-heading">{label('06 / ACADEMIC DEPARTMENTS')}<div><h2>PEOPLE BEHIND<br>YOUR LEARNING.</h2>{link('/management-team/', 'Explore our people', 'text-link')}</div></div><div class="home-department-grid">{team}</div><p class="home-source-note">Department names and roles follow BIT’s published program pages. Visit each program for its faculty list.</p></div></section>'''
    alumni = [
        ('Civil Engineering', 'Miss. Antima Yadav', '2073–2076', 'Sub-engineering', 'Water Supply, Irrigation and Energy Development Office, Salyan, Karnali'),
        ('Civil Engineering', 'Mr. Manoj Patel', '2065–2068', 'Civil engineering & project coordination', 'NSW Remedial Projects, Freyssinet Australia, Sydney'),
        ('Computer Engineering', 'Mr. Amit Chaurasiya', '2073–2076', 'Public service', 'District Police Office, Bhaktapur'),
        ('Computer Engineering', 'Er. Jitendra Chaudhary', '2069–2072', 'Software engineering', 'Fannie Mae, Dallas, Texas'),
        ('Mechanical Engineering', 'Mr. Dinesh Thakur', '2069–2072', 'Aviation technical support', 'Nepal Airlines Corporation'),
    ]
    rows = ''.join(f'<article class="alumni-pathway"><span>{icon("arrow-right-up")}</span><div><p class="alumni-program">{program} · Batch {batch} BS</p><h3>{name}</h3></div><div class="alumni-work"><strong>{role}</strong><p>{work}</p></div></article>' for program, name, batch, role, work in alumni)
    html += f'''<section class="section alumni-home"><div class="container"><div class="section-heading">{label('07 / ALUMNI PATHWAYS')}<div><h2>FROM BIT.<br>INTO THE WORLD.</h2><p class="heading-copy">Meet alumni highlighted by BIT across engineering, software, public service and aviation.</p></div></div><div class="alumni-pathways">{rows}</div><p class="home-source-note">Roles and organizations are those featured in BIT’s published alumni profiles.</p></div></section>'''
    campus = [('workshop-2.jpg', 'Sport & teamwork', 'Students taking part in BIT campus sports activities'), ('workshop-1.jpg', 'Events & community', 'A college community event at BIT'), ('industrial-visit.jpg', 'Industrial exposure', 'BIT students on an industrial visit')]
    images = ''.join(f'<a class="campus-story" href="/campus-life/">{photo(name, alt)}<span>{title}{icon("arrow-right-up")}</span></a>' for name, title, alt in campus)
    html += f'''<section class="section section-tint campus-home"><div class="container"><div class="section-heading">{label('08 / LIFE AT BIT')}<div><h2>MAKE YOUR COLLEGE<br>YEARS COUNT.</h2>{link('/campus-life/', 'Discover campus life', 'text-link')}</div></div><div class="campus-story-grid">{images}</div><div class="student-voices"><div>{label('STUDENT PERSPECTIVES')}<h3>Perspectives from the classroom.</h3><p>Student feedback from BIT’s original website, summarized here.</p></div><article><p>Nilu highlights support from the management and faculty during her Computer Engineering studies.</p><h3>Nilu Kumari</h3><span>Computer Engineering student</span></article><article><p>Aashik describes an encouraging learning environment, with attention from teachers and access to laboratories.</p><h3>Aashik Hawari</h3><span>Civil Engineering student</span></article></div></div></section>'''
    return html
