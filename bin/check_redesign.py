#!/usr/bin/env python3
"""Structural checks for the UCLA redesign, run against the built _site/.

Usage: python3 bin/check_redesign.py <group> [<group> ...]   (or "all")
Exits non-zero and lists every failed expectation.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
FAILURES = []


def expect(condition, message):
    if not condition:
        FAILURES.append(message)


def read_site(rel):
    return (SITE / rel).read_text(encoding="utf-8-sig")


def read_src(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------- source-data counts ----------


def bib_count(pattern):
    return len(re.findall(pattern, read_src("_bibliography/papers.bib"), flags=re.M | re.I))


def bib_entries():
    return bib_count(r"^@\w+\{")


def cv_field_count(section, field):
    """Count non-commented `field:` lines with a value inside a cv.yml section."""
    n, inside = 0, False
    for line in read_src("_data/cv.yml").splitlines():
        if re.match(r"^    \S", line):
            inside = line.strip() == f"{section}:"
        elif inside and re.match(rf"^\s+-?\s*{field}:\s*\S", line):
            n += 1
    return n


def research_area_anchors():
    return re.findall(r"^\s*anchor:\s*(\S+)", read_src("_data/research_areas.yml"), flags=re.M)


def news_count():
    return len(list((ROOT / "_news").glob("*.md")))


# ---------- html helpers ----------


def between(html, start_marker, end_marker):
    i = html.find(start_marker)
    if i < 0:
        return ""
    j = html.find(end_marker, i + len(start_marker))
    return html[i : j if j >= 0 else len(html)]


def home_section(html, name):
    return between(html, f'data-home-section="{name}"', "</section>")


def nav_labels(html):
    nav = between(html, '<ul class="navbar-nav', "</ul>")
    labels = re.findall(r'<a class="nav-link"[^>]*>\s*([^<]+?)\s*<', nav)
    return [re.sub(r"\s+", " ", label).strip() for label in labels]


# ---------- color contrast (WCAG 2.x) ----------


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def css_vars(css, selector_regex):
    m = re.search(selector_regex + r"\s*\{([^}]*)\}", css)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", m.group(1))) if m else {}


# ---------- groups ----------


def check_tokens():
    index = read_site("index.html")
    css = read_site("assets/css/main.css")
    expect("fonts.googleapis.com/css2?family=Inter" in index, "Google Fonts link does not load Inter (css2 API)")
    expect("Source+Serif+4" in index, "Google Fonts link does not load Source Serif 4")
    expect("Roboto+Slab" not in index, "old Roboto font link is still present")
    expect("Source Serif 4" in css and "Inter" in css, "main.css does not set the Inter / Source Serif 4 families")
    for mode, selector in (("light", r":root"), ("dark", r"html\[data-theme=[\"']?dark[\"']?\]")):
        tokens = css_vars(css, selector)
        bg = tokens.get("--global-bg-color", "").strip()
        expect(bg.startswith("#"), f"{mode}: --global-bg-color is not a hex color ({bg!r})")
        for name in (
            "--global-text-color",
            "--global-text-color-light",
            "--global-theme-color",
            "--global-heading-color",
            "--global-award-color",
        ):
            value = tokens.get(name, "").strip()
            if not value.startswith("#") or not bg.startswith("#"):
                expect(False, f"{mode}: {name} missing or not hex ({value!r})")
                continue
            ratio = contrast(value, bg)
            expect(ratio >= 4.5, f"{mode}: {name} {value} on {bg} has contrast {ratio:.2f} < 4.5")
        theme = tokens.get("--global-theme-color", "").strip().lower()
        expect(theme in ("#2774ae", "#8bb8e8"), f"{mode}: theme color is not UCLA blue ({theme})")
        expect("#b509ac" not in "".join(tokens.values()).lower(), f"{mode}: al-folio purple is still in the tokens")


# Broken before the redesign (origin/main 89b49bd): template tags/categories shown on the
# blog index without posts, and the unlinked people page. Only new breakage fails the check.
KNOWN_BROKEN = {
    "blog/index.html -> /blog/category/external-services",
    "blog/index.html -> /blog/tag/blockquotes",
    "blog/index.html -> /blog/tag/code",
    "blog/index.html -> /blog/tag/formatting",
    "blog/index.html -> /blog/tag/images",
    "blog/index.html -> /blog/tag/links",
    "blog/index.html -> /blog/tag/math",
    "people/index.html -> /al-folio/publications/",
}


def check_links():
    missing = set()
    for page in SITE.rglob("*.html"):
        if "assets" in page.relative_to(SITE).parts:
            continue
        for url in re.findall(r'(?:href|src)="(/[^"#?]*)', page.read_text(encoding="utf-8-sig", errors="ignore")):
            if url.startswith("//"):
                continue
            target = SITE / url.lstrip("/")
            if url.endswith("/"):
                target = target / "index.html"
            if not (target.exists() or target.with_suffix(".html").exists() or (target / "index.html").exists()):
                missing.add(f"{page.relative_to(SITE)} -> {url}")
    for item in sorted(missing - KNOWN_BROKEN):
        expect(False, f"broken internal link: {item}")
    # Anchor targets must be unique, e.g. /research/#<area> links from the homepage.
    for page in ("index.html", "research/index.html", "publications/index.html", "news/index.html", "blog/index.html", "cv/index.html", "404.html"):
        ids = re.findall(r'\sid="([^"]+)"', read_site(page))
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        expect(not dupes, f"{page}: duplicate ids {dupes}")


def check_nav():
    svg = SITE / "assets/img/logos/ucla-wordmark-white.svg"
    expect(svg.exists() and svg.read_text().count("<path") == 4, "UCLA wordmark SVG missing or not the 4-path original")
    css = read_site("assets/css/main.css").replace(" ", "")
    expect(re.search(r"\.brand-ucla\{[^}]*background-color:#2774ae", css) is not None, "UCLA box is not fixed UCLA Blue")
    for page in ("index.html", "publications/index.html", "cv/index.html"):
        html = read_site(page)
        brand = between(html, 'class="navbar-brand brand"', "</div>")
        expect("brand-ucla" in brand and "ucla-wordmark-white.svg" in brand, f"{page}: navbar brand has no UCLA box")
        expect("Peiran Wang" in brand, f"{page}: navbar brand does not show 'Peiran Wang'")
        expect("brand-lab" not in brand, f"{page}: lab logo rendered although lab_logo is unset")
        labels = nav_labels(html)
        expect(labels == ["Publications", "Research", "Blog", "CV"], f"{page}: nav labels are {labels}")
        expect('<progress id="progress"' not in html, f"{page}: scroll progress bar still rendered")


def check_home():
    html = read_site("index.html")
    hero = between(html, '<header class="hero">', "</header>")
    expect(re.search(r'<h1 class="hero-name">\s*Peiran Wang\s*</h1>', hero) is not None, "hero h1 is not 'Peiran Wang'")
    for text in (
        "Ph.D. Student",
        "Department of Computer Science",
        "University of California, Los Angeles",
        "Advisor: Prof. Yuan Tian",
        "UCLA Security Lab",
    ):
        expect(text in hero, f"hero is missing '{text}'")
    expect('href="https://ucla-sec.com/"' in hero, "hero does not link the lab site")
    links = between(hero, 'class="hero-links"', "</div>")
    expect("mailto:" in links and "ai-google-scholar" in links, "hero social links missing email / Scholar")
    expect('class="contact-icons"' not in html, "old bottom social block still rendered")
    rows = home_section(html, "news").count("<tr>")
    expected_rows = min(6, news_count())
    expect(rows == expected_rows, f"homepage news shows {rows} rows, expected {expected_rows}")
    expect('data-home-section="posts"' not in html, "latest posts section still on the homepage")
    expect('class="research-areas"' not in html, "old research-area card grid still on the homepage")
    selected = bib_count(r"^\s*selected\s*=\s*\{?true")
    pubs = home_section(html, "publications").count('<div class="title">')
    expect(pubs == selected, f"homepage shows {pubs} selected papers, papers.bib marks {selected}")
    expect(html.count('class="org-icon"') == 2, "bio should carry 2 inline org icons (UCLA, Sichuan University)")
    css = read_site("assets/css/main.css")
    for rule in (".hero{", ".hero-photo", ".section-title", ".home-section", ".org-icon{"):
        expect(rule in css, f"main.css is missing the homepage rule {rule!r}")


def check_sections():
    html = read_site("index.html")
    order = re.findall(r'data-home-section="([a-z]+)"', html)
    expect(order == ["news", "research", "publications", "awards", "experience"], f"homepage section order is {order}")
    research = home_section(html, "research")
    for anchor in research_area_anchors():
        expect(f'/research/#{anchor}"' in research, f"research interests missing link to /research/#{anchor}")
    awards = home_section(html, "awards").count("<li")
    award_entries = cv_field_count("Awards", "title")
    expect(awards == award_entries, f"homepage shows {awards} awards, cv.yml has {award_entries}")
    exp = home_section(html, "experience")
    jobs = cv_field_count("Experience", "company")
    expect(exp.count("<li") == jobs, f"homepage shows {exp.count('<li')} experience items, cv.yml has {jobs}")
    logos = cv_field_count("Experience", "logo")
    shown_logos = exp.count('class="org-logo"')
    expect(shown_logos == logos, f"experience shows {shown_logos} logos, cv.yml has {logos}")
    open_ended = cv_field_count("Experience", "start_date") - cv_field_count("Experience", "end_date")
    expect(exp.count("Present") == open_ended, f"expected {open_ended} 'Present' end dates in experience")


GROUPS = {
    "tokens": check_tokens,
    "links": check_links,
    "nav": check_nav,
    "home": check_home,
    "sections": check_sections,
}


def main(argv):
    names = list(GROUPS) if argv == ["all"] else argv
    if not names or any(n not in GROUPS for n in names):
        print(__doc__)
        print("groups:", ", ".join(GROUPS))
        return 2
    for name in names:
        before = len(FAILURES)
        GROUPS[name]()
        print(f"[{'PASS' if len(FAILURES) == before else 'FAIL'}] {name}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
