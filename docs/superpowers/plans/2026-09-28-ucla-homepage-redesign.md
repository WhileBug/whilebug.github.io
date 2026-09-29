# UCLA Homepage Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle the al-folio site after yrbding.github.io with a UCLA identity (flat single-page homepage, UCLA wordmark navbar, Source Serif 4 + Inter, UCLA colors in light and dark mode) without touching content or pipelines.

**Architecture:** Restyle in place. Color tokens live in `_sass/_themes.scss`; shared type and list styles in a new `_sass/_ucla.scss`; homepage styles in a new `_sass/_home.scss`. The homepage layout `_layouts/about.liquid` is rebuilt from small includes that read existing data (`about.md` front matter, `_news/`, `papers.bib`, `_data/cv.yml`, `_data/research_areas.yml`). Every task is verified by a stdlib-only Python checker that parses the built `_site/`, plus screenshots.

**Tech Stack:** Jekyll 4 (al-folio v0.16.3 Docker image), Liquid, SCSS (Dart Sass, compressed output), jekyll-scholar, Python 3.9 (checks), headless Chrome (screenshots), Prettier 3 with the Liquid plugin.

**Spec:** `docs/superpowers/specs/2026-09-28-ucla-homepage-redesign-design.md`

## Global Constraints

- Branch `ucla-redesign` (from `origin/main` 89b49bd). Never push; merging is the user's call.
- Colors, light / dark: bg `#FFFFFF` / `#0F1C27`; text `#1F2933` / `#E6EDF3`; muted `#5B6B7A` / `#9FB3C8`; theme+links `#2774AE` / `#8BB8E8`; headings `#003B5C` / `#DAEBFE`; accent `#FFD100` / `#FFD100`; award `#8A6500` / `#FFD100`; divider `rgba(0,0,0,.1)` / `rgba(255,255,255,.12)`.
- Gold (`#FFD100`) is decorative only (underlines, rules) and never used for body text on white.
- Every text token has contrast ≥ 4.5:1 on its background.
- Fonts: Source Serif 4 for headings, page titles, section titles, navbar name; Inter for body/UI. Loaded from `https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300..700;1,14..32,300..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap`.
- Content width stays `max_width: 930px`.
- No content text changes (bio, news, papers, CV). `_data/socials.yml` stays as is.
- Before every commit: `npx prettier --write --ignore-unknown <files you touched>` (AGENTS.md; do not reformat unrelated files), stage files explicitly, message `<type>: <subject>` (`.github/GIT_WORKFLOW.md`) ending with the trailer `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
- Checker scripts use only the Python 3.9 standard library (macOS system Python): no backslashes inside f-string `{}` expressions.
- Local site: `docker compose up -d` serves <http://localhost:8080> and rebuilds on change. After every edit run `bin/wait_for_build.sh` before checks or screenshots.
- Screenshots go to `SHOTS=${TMPDIR:-/tmp}/ucla-redesign-shots` (outside the repo).

## Review Focus

1. **Production CSS purge.** `deploy.yml` runs `purgecss` after a production build; any new selector missing from the HTML/JS would silently disappear on the live site. Expect the purged production build to pass the same checks and look the same (Task 6, Step 6).
2. **Lab logo turned on later.** Setting `lab_logo` in `_config.yml` must render a separate link to the lab site next to the UCLA box, not a link nested inside the home link (Task 2, Step 6).
3. **CV entries missing optional fields.** An Experience entry without `logo` must render without a broken image, and an empty `end_date` must read "Present" (Task 4 check counts logos against entries that have one).
4. **Phones (390px).** Navbar brand plus menu button and the hero must fit without horizontal scrolling; the photo stacks above the name (Tasks 2 and 3 phone screenshots, explicit pass criteria).
5. **First visit in system dark mode** (the user's Mac is in dark mode). All new colors must stay readable and the UCLA box must stay UCLA Blue (Task 1 contrast check for both themes; Task 2 check on the box color).

---

## File Map

| Action | File                                             | Responsibility                                                |
| ------ | ------------------------------------------------ | ------------------------------------------------------------- |
| Create | `bin/check_redesign.py`                          | Structural checks against `_site/`, one group per task        |
| Create | `bin/wait_for_build.sh`                          | Trigger a rebuild and wait for the container to finish it     |
| Create | `bin/shoot_pages.sh`                             | Screenshots of 7 pages, desktop + phone, light + dark         |
| Modify | `_sass/_themes.scss`                             | UCLA color tokens (light and dark)                            |
| Create | `_sass/_ucla.scss`                               | Fonts, heading color, news list, figure radius                |
| Create | `_sass/_home.scss`                               | Hero, section heads, homepage lists                           |
| Modify | `assets/css/main.scss`                           | `@use` the two new partials                                   |
| Modify | `_config.yml`                                    | Fonts URL, progress bar off, `lab_logo` example, footer flags |
| Create | `assets/img/logos/ucla-wordmark-white.svg`       | Official UCLA wordmark (white)                                |
| Modify | `_includes/header.liquid`                        | Brand block, drop "about" item                                |
| Modify | `_sass/_navbar.scss`                             | Brand styles, gold active underline, no opacity               |
| Modify | `_pages/{publications,research,blog,cv,news}.md` | Capitalized titles, nav order                                 |
| Modify | `_pages/about.md`                                | Hero data, section flags, inline org icons                    |
| Modify | `_layouts/about.liquid`                          | Homepage section structure                                    |
| Create | `_includes/home/hero.liquid`                     | Name, affiliation blocks, social icons, photo                 |
| Create | `_includes/research_interests.liquid`            | Compact research-area list                                    |
| Create | `_includes/home/awards.liquid`                   | Awards from `cv.yml`                                          |
| Create | `_includes/home/experience.liquid`               | Experience from `cv.yml`                                      |
| Modify | `_layouts/bib.liquid`                            | Thumbnail column, award line, "Cited by N"                    |
| Modify | `_sass/_publications.scss`                       | Paper list styles                                             |
| Modify | `_sass/_footer.scss`                             | Light end-of-page footer                                      |

---

### Task 1: Check tooling, color tokens, and fonts

**Files:**

- Create: `bin/check_redesign.py`, `bin/wait_for_build.sh`, `bin/shoot_pages.sh`, `_sass/_ucla.scss`
- Modify: `_sass/_themes.scss` (`:root` and `html[data-theme="dark"]` token lines), `assets/css/main.scss`, `_config.yml` (`google_fonts` URL)

**Interfaces:**

- Produces: `python3 bin/check_redesign.py <group>...` with groups `tokens`, `links` (later tasks add `nav`, `home`, `sections`, `pubs`, `pages`); helpers `expect`, `read_site`, `read_src`, `bib_count`, `bib_entries`, `cv_field_count`, `research_area_anchors`, `news_count`, `between`, `home_section`, `nav_labels`, `css_vars`, `contrast`, and the `GROUPS` dict. CSS custom properties `--global-heading-color`, `--global-accent-color`, `--global-award-color` (both themes). `bin/wait_for_build.sh`, `bin/shoot_pages.sh <out-dir> [base-url]`.

- [ ] **Step 1: Start the dev server**

```bash
docker compose up -d
```

Expected: container `whilebuggithubio-jekyll-1` started; <http://localhost:8080> returns 200 within about 30 s.

- [ ] **Step 2: Create `bin/wait_for_build.sh`**

```bash
#!/usr/bin/env bash
# Trigger a rebuild of the running jekyll container and wait until it finishes.
# Exits 1 (and prints the log lines) if Jekyll reports a Liquid/Sass error.
set -euo pipefail

since=$(date -u +%Y-%m-%dT%H:%M:%SZ)
touch _pages/about.md
for _ in $(seq 1 150); do
  logs=$(docker compose logs --no-color --since "$since" jekyll 2>&1 || true)
  if grep -qE "Liquid (Exception|Warning)|Conversion error|[^_]Error:" <<<"$logs"; then
    echo "BUILD ERROR:"
    grep -E "Liquid (Exception|Warning)|Conversion error|[^_]Error:" <<<"$logs" | head -20
    exit 1
  fi
  if grep -q "done in" <<<"$logs"; then
    echo "build finished"
    exit 0
  fi
  sleep 2
done
echo "timed out waiting for the build"
exit 1
```

- [ ] **Step 3: Create `bin/shoot_pages.sh`**

```bash
#!/usr/bin/env bash
# Screenshot the main pages in light and dark mode, at desktop (1400px) and phone (390px) width.
# Usage: bin/shoot_pages.sh <out-dir> [base-url]   (default base-url: http://localhost:8080)
set -euo pipefail

mkdir -p "${1:?usage: bin/shoot_pages.sh <out-dir> [base-url]}"
out="$(cd "$1" && pwd)"
base="${2:-http://localhost:8080}"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pages="home:/ publications:/publications/ research:/research/ news:/news/ blog:/blog/ cv:/cv/ 404:/404.html"

for entry in $pages; do
  name="${entry%%:*}"
  path="${entry#*:}"
  # Headless Chrome cannot render narrower than 500px, so phones use a 390px iframe.
  printf '<!doctype html><body style="margin:0"><iframe src="%s%s" width="390" height="2400" style="border:0"></iframe>' \
    "$base" "$path" >"$out/$name-phone.html"
  for mode in light dark; do
    scheme=1
    [ "$mode" = dark ] && scheme=0
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --blink-settings=preferredColorScheme=$scheme \
      --virtual-time-budget=8000 --window-size=1400,2400 \
      --screenshot="$out/$name-desktop-$mode.png" "$base$path" 2>/dev/null
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --blink-settings=preferredColorScheme=$scheme \
      --virtual-time-budget=8000 --window-size=500,2400 \
      --screenshot="$out/$name-phone-$mode.png" "file://$out/$name-phone.html" 2>/dev/null
  done
done
echo "screenshots in $out"
```

Then `chmod +x bin/wait_for_build.sh bin/shoot_pages.sh` and take the baseline: `SHOTS=${TMPDIR:-/tmp}/ucla-redesign-shots; bin/shoot_pages.sh "$SHOTS/0-baseline"`. Expected: 28 PNGs.

- [ ] **Step 4: Create `bin/check_redesign.py` (the failing test)**

```python
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


GROUPS = {
    "tokens": check_tokens,
    "links": check_links,
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
```

- [ ] **Step 5: Run it to verify `tokens` fails and `links` passes**

Run: `python3 bin/check_redesign.py tokens links`
Expected: `[FAIL] tokens` (Inter / Source Serif 4 missing, Roboto present, `#828282` muted text at 3.84 < 4.5, heading/award tokens missing, theme not UCLA blue) and `[PASS] links`.

- [ ] **Step 6: Set the color tokens in `_sass/_themes.scss`**

In the `:root` block replace

```scss
--global-bg-color: #{v.$white-color};
--global-code-bg-color: #{v.$code-bg-color-light};
--global-text-color: #{v.$black-color};
--global-text-color-light: #{v.$grey-color};
--global-theme-color: #{v.$purple-color};
--global-hover-color: #{v.$purple-color};
```

with

```scss
--global-bg-color: #ffffff;
--global-code-bg-color: rgba(39, 116, 174, 0.06);
--global-text-color: #1f2933;
--global-text-color-light: #5b6b7a;
--global-theme-color: #2774ae;
--global-hover-color: #2774ae;
--global-heading-color: #003b5c;
--global-accent-color: #ffd100;
--global-award-color: #8a6500;
```

In the `html[data-theme="dark"]` block replace

```scss
--global-bg-color: #{v.$grey-color-dark};
--global-code-bg-color: #{v.$code-bg-color-dark};
--global-text-color: #{v.$grey-color-light};
--global-text-color-light: #{v.$grey-color};
--global-theme-color: #{v.$cyan-color};
--global-hover-color: #{v.$cyan-color};
```

with

```scss
--global-bg-color: #0f1c27;
--global-code-bg-color: #{v.$code-bg-color-dark};
--global-text-color: #e6edf3;
--global-text-color-light: #9fb3c8;
--global-theme-color: #8bb8e8;
--global-hover-color: #8bb8e8;
--global-heading-color: #daebfe;
--global-accent-color: #ffd100;
--global-award-color: #ffd100;
```

and in the same dark block change `--global-divider-color: #424246;` to `--global-divider-color: rgba(255, 255, 255, 0.12);` and `--global-card-bg-color: #{v.$grey-900};` to `--global-card-bg-color: #132636;`.

- [ ] **Step 7: Create `_sass/_ucla.scss`**

```scss
/*******************************************************************************
 * UCLA redesign: fonts, heading colors, and styles shared across pages
 ******************************************************************************/

$font-sans:
  "Inter",
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  Roboto,
  "Helvetica Neue",
  Arial,
  sans-serif;
$font-serif: "Source Serif 4", Georgia, "Times New Roman", serif;

body {
  font-family: $font-sans;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1,
h2,
h3,
h4,
h5,
h6,
.post-title {
  font-family: $font-serif;
}

h1,
h2,
h3,
.post-title {
  color: var(--global-heading-color);
  font-weight: 600;
}
```

In `assets/css/main.scss` add after `@use "cv";`:

```scss
@use "ucla";
```

- [ ] **Step 8: Switch the Google Fonts URL in `_config.yml`**

Replace

```yaml
fonts: "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Roboto+Slab:100,300,400,500,700|Material+Icons&display=swap"
```

with

```yaml
fonts: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300..700;1,14..32,300..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap"
```

(Material Icons is not referenced anywhere; `grep -rn "material-icons" _includes _layouts _pages _posts _sass assets/js` must print nothing. If it prints something, keep `&family=Material+Icons` at the end of the new URL.)

- [ ] **Step 9: Rebuild and verify the checks pass**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py tokens links`
Expected: `build finished`, `[PASS] tokens`, `[PASS] links`.

- [ ] **Step 10: Screenshots**

Run: `bin/shoot_pages.sh "$SHOTS/1-tokens"`. Open `home-desktop-light.png` and `home-desktop-dark.png`. Expected: headings in Source Serif 4 (serifs visible), body in Inter, links UCLA blue (light) / light blue (dark), dark background navy `#0F1C27`, no purple anywhere.

- [ ] **Step 11: Format and commit**

```bash
npx prettier --write --ignore-unknown _sass/_themes.scss _sass/_ucla.scss assets/css/main.scss _config.yml
git add bin/check_redesign.py bin/wait_for_build.sh bin/shoot_pages.sh _sass/_themes.scss _sass/_ucla.scss assets/css/main.scss _config.yml
git commit -F - <<'EOF'
style: Add UCLA color tokens, Inter + Source Serif 4, and redesign checks

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

---

### Task 2: Navbar with the UCLA wordmark

**Files:**

- Create: `assets/img/logos/ucla-wordmark-white.svg`
- Modify: `_includes/header.liquid` (brand block at the top of `.container`; the "About" item in `.navbar-nav`), `_sass/_navbar.scss`, `_config.yml` (`enable_progressbar`, `lab_logo` example), `_pages/publications.md`, `_pages/research.md`, `_pages/blog.md`, `_pages/cv.md`, `bin/check_redesign.py`

**Interfaces:**

- Consumes: `--global-heading-color`, `--global-accent-color`, `--global-theme-color` (Task 1); checker helpers `between`, `nav_labels`, `read_site`, `expect`, `GROUPS`.
- Produces: brand markup `<div class="navbar-brand brand">` containing `a.brand-ucla > img`, optional `a.brand-lab`, `a.brand-name`; `_config.yml` key `lab_logo: {image, url, alt}` (unset by default); check group `nav`.

- [ ] **Step 1: Add the `nav` check group (failing test)**

In `bin/check_redesign.py` add above `GROUPS = {`:

```python
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
```

and add `"nav": check_nav,` to `GROUPS`.

Run: `python3 bin/check_redesign.py nav`
Expected: `[FAIL] nav` — SVG missing, no UCLA box, labels `['about', 'blog', 'publications', 'research', 'CV']`, progress bar rendered.

- [ ] **Step 2: Add the official UCLA wordmark**

```bash
mkdir -p assets/img/logos
curl -sL https://brand.ucla.edu/images/logo-ucla.svg -o assets/img/logos/ucla-wordmark-white.svg
grep -c "<path" assets/img/logos/ucla-wordmark-white.svg   # expect 4
grep -o "fill:#fff" assets/img/logos/ucla-wordmark-white.svg # expect fill:#fff
```

Do not edit the SVG.

- [ ] **Step 3: Replace the brand block and drop the "About" item in `_includes/header.liquid`**

Replace everything from `{% if page.permalink != '/' %}` down to its `{% endif %}` (the block ending with `<div class="navbar-brand social">{% social_links %}</div>`, just above `<!-- Navbar Toggle -->`) with:

```liquid
<div class="navbar-brand brand">
  <a class="brand-ucla" href="{{ '/' | relative_url }}" aria-label="Home">
    <img src="{{ '/assets/img/logos/ucla-wordmark-white.svg' | relative_url }}" alt="UCLA" width="55" height="18">
  </a>
  {% if site.lab_logo and site.lab_logo.image %}
    <a class="brand-lab" href="{{ site.lab_logo.url }}">
      <img src="{{ site.lab_logo.image | relative_url }}" alt="{{ site.lab_logo.alt }}" height="30">
    </a>
  {% endif %}
  <a class="brand-name" href="{{ '/' | relative_url }}">
    {{- site.first_name }}
    {{ site.last_name -}}
  </a>
</div>
```

Then delete this block inside `<ul class="navbar-nav ml-auto flex-nowrap">` (keep the `<!-- Other pages -->` comment and everything after it):

```liquid
{% for page in site.pages %}
  {% if page.permalink == '/' %} {% assign about_title = page.title %} {% endif %}
{% endfor %}

<!-- About -->
<li class="nav-item {% if page.permalink == '/' %}active{% endif %}">
  <a class="nav-link" href="{{ '/' | relative_url }}">
    {{- about_title }}
    {% if page.permalink == '/' %}
      <span class="sr-only">(current)</span>
    {% endif %}
  </a>
</li>
```

- [ ] **Step 4: Navbar styles in `_sass/_navbar.scss`**

In the `.navbar { … }` rule delete the line `opacity: 0.95;`.

In `.navbar.navbar-light { … }` change the active-item rule to:

```scss
.navbar-nav .nav-item.active > .nav-link {
  background-color: inherit;
  font-weight: 600;
  color: var(--global-theme-color);
  box-shadow: inset 0 -3px 0 var(--global-accent-color);

  &:hover {
    color: var(--global-hover-color);
  }
}
```

Append at the end of the file:

```scss
// UCLA brand: wordmark box, optional lab logo, name
.navbar .brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-right: 1rem;
  padding: 0;
}

.brand-ucla {
  display: inline-flex;
  align-items: center;
  padding: 6px 9px;
  background-color: #2774ae; // UCLA Blue in both themes

  img {
    display: block;
    height: 18px;
    width: auto;
  }
}

.brand-lab img {
  display: block;
  height: 30px;
  width: auto;
}

.navbar.navbar-light .brand-name {
  font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--global-heading-color);
  white-space: nowrap;

  &:hover {
    color: var(--global-theme-color);
    text-decoration: none;
  }
}
```

- [ ] **Step 5: Config and page front matter**

`_config.yml`: change `enable_progressbar: true` to `enable_progressbar: false` (keep its comment), and add right after the `navbar_fixed: true` line:

```yaml
# Optional lab logo next to the UCLA box in the navbar (leave commented to hide it)
# lab_logo:
#   image: /assets/img/logos/lab.svg
#   url: https://ucla-sec.com/
#   alt: UCLA Security Lab
```

Front matter edits (nothing else in these files changes):

| File                     | `title:`                        | `nav_order:` |
| ------------------------ | ------------------------------- | ------------ |
| `_pages/publications.md` | `publications` → `Publications` | `2` → `1`    |
| `_pages/research.md`     | `research` → `Research`         | stays `2`    |
| `_pages/blog.md`         | `blog` → `Blog`                 | `1` → `3`    |
| `_pages/cv.md`           | stays `CV`                      | `5` → `4`    |

- [ ] **Step 6: Rebuild, verify, and pin the lab-logo case**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py tokens nav links`
Expected: all three `[PASS]`.

Lab-logo case (Review Focus 2): temporarily uncomment the `lab_logo` block in `_config.yml` and set `image: /assets/img/badges/UCLA.png`, then:

```bash
bin/wait_for_build.sh && python3 - <<'EOF'
import re
html = open("_site/index.html", encoding="utf-8-sig").read()
brand = html[html.find('class="navbar-brand brand"'):]
brand = brand[: brand.find("</div>")]
lab = re.search(r'<a class="brand-lab" href="https://ucla-sec.com/"', brand)
assert lab, "lab logo link missing"
before = brand[: lab.start()]
assert before.count("<a ") == before.count("</a>"), "lab link is nested inside another link"
print("lab logo OK")
EOF
```

Expected: `lab logo OK`. Then restore the commented block exactly as in Step 5, run `bin/wait_for_build.sh && python3 bin/check_redesign.py nav` again → `[PASS] nav`, and confirm `git diff _config.yml` shows only the Step 5 changes.

- [ ] **Step 7: Screenshots**

Run: `bin/shoot_pages.sh "$SHOTS/2-nav"`. Pass criteria: on `home-desktop-light.png` and `-dark.png` the left of the navbar shows the white UCLA wordmark in a blue box and "Peiran Wang" in serif; right side reads Publications / Research / Blog / CV, search, theme toggle; the active page (open `publications-desktop-light.png`) has a gold underline; no progress bar. On `home-phone-light.png` the brand and the menu button fit on one line with no horizontal cut-off.

- [ ] **Step 8: Format and commit**

```bash
npx prettier --write --ignore-unknown _includes/header.liquid _sass/_navbar.scss _config.yml _pages/publications.md _pages/research.md _pages/blog.md _pages/cv.md
git add assets/img/logos/ucla-wordmark-white.svg _includes/header.liquid _sass/_navbar.scss _config.yml _pages/publications.md _pages/research.md _pages/blog.md _pages/cv.md bin/check_redesign.py
git commit -F - <<'EOF'
feat: Add UCLA wordmark navbar with name and gold active underline

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

---

### Task 3: Homepage hero, bio, and news

**Files:**

- Create: `_includes/home/hero.liquid`, `_sass/_home.scss`
- Modify: `_layouts/about.liquid` (whole file), `_pages/about.md` (whole file), `_sass/_ucla.scss` (append news styles), `assets/css/main.scss`, `bin/check_redesign.py`

**Interfaces:**

- Consumes: tokens from Task 1; checker helpers `between`, `home_section`, `bib_count`, `news_count`.
- Produces: `about.md` front matter `profile.image`, `profile.blocks[].lines[].{text,url}`; homepage sections `<section class="home-section" data-home-section="<name>">` with a `.section-head` (`h2.section-title` + optional `a.section-more`); CSS classes `.hero*`, `.home-section`, `.section-head`, `.section-title`, `.section-more`, `.org-icon`; check group `home`.

- [ ] **Step 1: Add the `home` check group (failing test)**

In `bin/check_redesign.py` add above `GROUPS = {`:

```python
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
```

and add `"home": check_home,` to `GROUPS`.

Run: `python3 bin/check_redesign.py home`
Expected: `[FAIL] home` (no hero, old social block, 5 news rows, latest posts present, card grid present, 0 org icons).

- [ ] **Step 2: Create `_includes/home/hero.liquid`**

```liquid
<header class="hero">
  <div class="hero-text">
    <h1 class="hero-name">
      {{ site.first_name }}
      {{ site.last_name }}
    </h1>
    {% for block in page.profile.blocks %}
      <p class="hero-block">
        {% for line in block.lines %}
          {% if line.url -%}
            <a href="{{ line.url }}">{{ line.text }}</a>
          {%- else -%}
            {{- line.text -}}
          {%- endif %}
          {% unless forloop.last %}<br>{% endunless %}
        {% endfor %}
      </p>
    {% endfor %}
    {% if page.social %}
      <div class="hero-links">{% social_links %}</div>
    {% endif %}
  </div>
  {% if page.profile.image %}
    {% assign profile_image_path = page.profile.image | prepend: 'assets/img/' %}
    <div class="hero-photo">
      {%
        include figure.liquid loading="eager" path=profile_image_path class="img-fluid" sizes="200px" alt="Portrait of Peiran Wang"
        cache_bust=true
      %}
    </div>
  {% endif %}
</header>
```

- [ ] **Step 3: Replace `_layouts/about.liquid`**

```liquid
---
layout: default
---
<div class="post home">
  {% include home/hero.liquid %}

  <article>
    <div class="home-bio clearfix">{{ content }}</div>

    <!-- News -->
    {% if page.announcements and page.announcements.enabled %}
      <section class="home-section" data-home-section="news">
        <div class="section-head">
          <h2 class="section-title">News</h2>
          <a class="section-more" href="{{ '/news/' | relative_url }}">All news &rarr;</a>
        </div>
        {% include news.liquid limit=true %}
      </section>
    {% endif %}

    <!-- Latest posts (off in about.md; kept so it can be switched back on) -->
    {% if page.latest_posts and page.latest_posts.enabled %}
      <section class="home-section" data-home-section="posts">
        <div class="section-head">
          <h2 class="section-title">Latest Posts</h2>
          <a class="section-more" href="{{ '/blog/' | relative_url }}">Blog &rarr;</a>
        </div>
        {% include latest_posts.liquid %}
      </section>
    {% endif %}

    <!-- Selected papers -->
    {% if page.selected_papers %}
      <section class="home-section" data-home-section="publications">
        <div class="section-head">
          <h2 class="section-title">Selected Publications</h2>
          <a class="section-more" href="{{ '/publications/' | relative_url }}">Full list &rarr;</a>
        </div>
        {% include selected_papers.liquid %}
      </section>
    {% endif %}

    {% if site.newsletter and site.newsletter.enabled and site.footer_fixed %}
      {% include newsletter.liquid center=true %}
    {% endif %}
  </article>
</div>
```

- [ ] **Step 4: Replace `_pages/about.md`**

The four bio lines keep their exact wording; only the two `<img class="org-icon">` tags are new.

```markdown
---
layout: about
title: about
permalink: /

profile:
  image: prof_pic.jpg
  blocks:
    - lines:
        - text: Ph.D. Student
        - text: Department of Computer Science
          url: https://www.cs.ucla.edu/
        - text: University of California, Los Angeles
          url: https://www.ucla.edu/
    - lines:
        - text: "Advisor: Prof. Yuan Tian"
        - text: UCLA Security Lab
          url: https://ucla-sec.com/

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # shows the icons from _data/socials.yml under the hero

announcements:
  enabled: true # includes a list of news items
  scrollable: false # the homepage list is short, so no inner scroll bar
  limit: 6 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false # the blog stays in the navbar; set to true to list posts here
  scrollable: true
  limit: 3

research_areas:
  enabled: true # compact list of _data/research_areas.yml, linking to /research/
---

I'm Peiran Wang (王沛然 in Chinese, you can speak as "Pay-than, Wang"), a CS PhD student in UCLA<img class="org-icon" src="{{ '/assets/img/badges/UCLA.png' | relative_url }}" alt="">.
I am currently interested in general AI Security (including LLM security, privacy, etc. Especially system security for LLM recently), Machine Learning System (MLSys), usable security, fraud detection and program analysis, etc.
I graduated from Sichuan University<img class="org-icon" src="{{ '/assets/img/badges/SCU.png' | relative_url }}" alt=""> in Cybersecurity Talented Class in 2022 (18/172). During my undergraduate, I got National Scholarship (3/172), and got GPA of 3.92 (rank 2/172).
I'm currently a CS PhD student in UCLA, under the supervision of Prof. Yuan Tian.
```

- [ ] **Step 5: Create `_sass/_home.scss` and register it**

```scss
/*******************************************************************************
 * Homepage (about layout): hero, section heads
 ******************************************************************************/

.hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 2rem;
  margin: 1.5rem 0;
}

.hero-name {
  font-size: 2.2rem;
  margin: 0 0 1rem;
}

.hero .hero-block {
  border-left: 2px solid var(--global-divider-color);
  padding-left: 0.9rem;
  margin: 0 0 0.9rem;
  line-height: 1.55;
  color: var(--global-text-color-light);
}

.hero-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.4rem;
  font-size: 1.35rem;

  a {
    color: var(--global-theme-color);

    &:hover {
      color: var(--global-hover-color);
      text-decoration: none;
    }
  }
}

.hero-photo {
  flex: 0 0 200px;

  figure {
    margin: 0;
  }

  img {
    width: 200px;
    max-width: none;
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  }
}

.org-icon {
  height: 1em;
  width: auto;
  margin-left: 0.2em;
  vertical-align: -0.12em;
}

.home-section {
  margin-top: 2.5rem;

  .publications {
    margin-top: 0;
  }
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  border-bottom: 1px solid var(--global-divider-color);
  padding-bottom: 0.35rem;
  margin-bottom: 0.9rem;
}

.section-title {
  position: relative;
  font-size: 1.5rem;
  margin: 0;

  // short gold rule sitting on the divider line
  &::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: calc(-0.35rem - 2px);
    width: 2.5rem;
    height: 3px;
    background-color: var(--global-accent-color);
  }
}

.section-more {
  font-size: 0.9rem;
  white-space: nowrap;
}

@media (max-width: 576px) {
  .hero {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .hero-photo {
    flex-basis: auto;

    img {
      width: 140px;
    }
  }
}
```

In `assets/css/main.scss` add after `@use "ucla";`:

```scss
@use "home";
```

- [ ] **Step 6: News list styles (shared with `/news/`) — append to `_sass/_ucla.scss`**

```scss
// News: date | text rows separated by hairlines (homepage and /news/)
.news table {
  width: 100%;
  margin-bottom: 0;

  th,
  td {
    padding: 0.55rem 1rem 0.55rem 0;
    vertical-align: top;
  }

  tr + tr th,
  tr + tr td {
    border-top: 1px solid var(--global-divider-color);
  }

  th {
    font-weight: 500;
    color: var(--global-text-color-light);
    white-space: nowrap;
  }
}
```

- [ ] **Step 7: Rebuild and verify**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py tokens nav home links`
Expected: all `[PASS]`.

- [ ] **Step 8: Screenshots**

Run: `bin/shoot_pages.sh "$SHOTS/3-home"`. Pass criteria for `home-desktop-light.png` / `-dark.png`: "Peiran Wang" large serif on the left, two affiliation blocks with thin left rules, icons row (CV, email, Scholar, RSS), photo on the right with rounded corners; bio with two small logos; "News" title with a short gold rule on the divider and "All news →" at the right; 6 news rows with hairlines; "Selected Publications" follows; no research cards, no latest posts, no big icon row at the bottom. For `home-phone-light.png`: photo on top, then name and blocks, no horizontal cut-off. Also open `news-desktop-light.png`: same row style.

- [ ] **Step 9: Format and commit**

```bash
npx prettier --write --ignore-unknown _includes/home/hero.liquid _layouts/about.liquid _pages/about.md _sass/_home.scss _sass/_ucla.scss assets/css/main.scss
git add _includes/home/hero.liquid _layouts/about.liquid _pages/about.md _sass/_home.scss _sass/_ucla.scss assets/css/main.scss bin/check_redesign.py
git commit -F - <<'EOF'
feat: Rebuild homepage with hero, affiliation blocks, and flat news list

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

---

### Task 4: Homepage research interests, awards, and experience

**Files:**

- Create: `_includes/research_interests.liquid`, `_includes/home/awards.liquid`, `_includes/home/experience.liquid`
- Modify: `_layouts/about.liquid` (two insertions), `_pages/about.md` (two front matter flags), `_sass/_home.scss` (append), `bin/check_redesign.py`

**Interfaces:**

- Consumes: section markup contract from Task 3 (`section.home-section[data-home-section]`, `.section-head`, `.section-title`); `site.data.research_areas[].{name,description,anchor}`; `site.data.cv.cv.sections.Awards[].{title,awarder,date}` and `.Experience[].{company,position,start_date,end_date,logo}`.
- Produces: `about.md` flags `awards: true`, `experience: true`; section names `research`, `awards`, `experience`; classes `.interest-list`, `.plain-list`, `.item-date`, `.org-logo`; check group `sections`.

- [ ] **Step 1: Add the `sections` check group (failing test)**

In `bin/check_redesign.py` add above `GROUPS = {`:

```python
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
```

`cv_field_count` only counts fields with a value, so an empty `end_date:` counts as open-ended and an entry without `logo:` must not render an `<img>` (Review Focus 3).

Then add `"sections": check_sections,` to `GROUPS`.

Run: `python3 bin/check_redesign.py sections`
Expected: `[FAIL] sections` (order `['news', 'publications']`, research links missing, 0 awards, 0 experience items).

- [ ] **Step 2: Create `_includes/research_interests.liquid`**

```liquid
<ul class="interest-list">
  {% for area in site.data.research_areas %}
    <li>
      <a href="{{ '/research/' | relative_url }}#{{ area.anchor }}">{{ area.name }}</a>
      <span class="interest-desc">{{ area.description }}</span>
    </li>
  {% endfor %}
</ul>
```

- [ ] **Step 3: Create `_includes/home/awards.liquid`**

```liquid
<ul class="plain-list">
  {% for award in site.data.cv.cv.sections.Awards %}
    <li>
      <span
        ><strong>{{ award.title }}</strong>{% if award.awarder %}, {{ award.awarder }}{% endif %}.</span
      >
      <span class="item-date">{{ award.date }}</span>
    </li>
  {% endfor %}
</ul>
```

- [ ] **Step 4: Create `_includes/home/experience.liquid`**

```liquid
<ul class="plain-list">
  {% for job in site.data.cv.cv.sections.Experience %}
    <li>
      <span>
        {%- if job.logo -%}
          <img class="org-logo" src="{{ job.logo | prepend: '/assets/img/' | relative_url }}" alt="" loading="lazy">
        {%- endif -%}
        {{ job.position }} @ {{ job.company }}
      </span>
      <span class="item-date">
        {{- job.start_date | date: '%b %Y' }} &ndash;
        {% if job.end_date %}{{ job.end_date | date: '%b %Y' }}{% else %}Present{% endif -%}
      </span>
    </li>
  {% endfor %}
</ul>
```

- [ ] **Step 5: Insert the sections into `_layouts/about.liquid`**

Insert directly before `<!-- Latest posts (off in about.md; kept so it can be switched back on) -->`:

```liquid
<!-- Research interests -->
{% if page.research_areas and page.research_areas.enabled %}
  <section class="home-section" data-home-section="research">
    <div class="section-head">
      <h2 class="section-title">Research Interests</h2>
      <a class="section-more" href="{{ '/research/' | relative_url }}">Details &rarr;</a>
    </div>
    {% include research_interests.liquid %}
  </section>
{% endif %}
```

Insert directly before `{% if site.newsletter and site.newsletter.enabled and site.footer_fixed %}`:

```liquid
<!-- Honors & awards -->
{% if page.awards %}
  <section class="home-section" data-home-section="awards">
    <div class="section-head">
      <h2 class="section-title">Honors &amp; Awards</h2>
    </div>
    {% include home/awards.liquid %}
  </section>
{% endif %}

<!-- Experience -->
{% if page.experience %}
  <section class="home-section" data-home-section="experience">
    <div class="section-head">
      <h2 class="section-title">Experience</h2>
      <a class="section-more" href="{{ '/cv/' | relative_url }}">Full CV &rarr;</a>
    </div>
    {% include home/experience.liquid %}
  </section>
{% endif %}
```

In `_pages/about.md` front matter add after the `social:` line:

```yaml
awards: true # Honors & Awards from _data/cv.yml
experience: true # Experience from _data/cv.yml
```

- [ ] **Step 6: List styles — append to `_sass/_home.scss`**

```scss
.interest-list,
.plain-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.interest-list li {
  padding: 0.3rem 0;

  a {
    font-weight: 600;
    margin-right: 0.35rem;
  }

  .interest-desc {
    color: var(--global-text-color-light);
    font-size: 0.92rem;
  }
}

.plain-list li {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.3rem 0;
}

.plain-list .item-date {
  color: var(--global-text-color-light);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.org-logo {
  width: 1.2rem;
  height: 1.2rem;
  object-fit: contain;
  margin-right: 0.5rem;
  vertical-align: -0.25em;
}
```

- [ ] **Step 7: Rebuild and verify**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py tokens nav home sections links`
Expected: all `[PASS]` (research 6 links, 5 awards, 11 experience items with 11 logos, 1 "Present").

- [ ] **Step 8: Screenshots**

Run: `bin/shoot_pages.sh "$SHOTS/4-sections"`. Pass criteria for `home-desktop-light.png` / `-dark.png`: sections in order News, Research Interests, Selected Publications, Honors & Awards, Experience; research lines are bold links with muted descriptions; awards and experience are one line each with the date right-aligned; experience rows have small logos; UCLA row ends in "Present". Phone screenshot: dates wrap below or stay right without horizontal cut-off.

- [ ] **Step 9: Format and commit**

```bash
npx prettier --write --ignore-unknown _includes/research_interests.liquid _includes/home/awards.liquid _includes/home/experience.liquid _layouts/about.liquid _pages/about.md _sass/_home.scss
git add _includes/research_interests.liquid _includes/home/awards.liquid _includes/home/experience.liquid _layouts/about.liquid _pages/about.md _sass/_home.scss bin/check_redesign.py
git commit -F - <<'EOF'
feat: Add research interests, awards, and experience to the homepage

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

---

### Task 5: Publication list (Publications page and homepage)

**Files:**

- Modify: `_layouts/bib.liquid` (thumbnail column, text column, award line, citation badge, hidden award block), `_sass/_publications.scss` (whole file), `bin/check_redesign.py`

**Interfaces:**

- Consumes: tokens `--global-theme-color`, `--global-award-color`, `--global-heading-color`, `--global-divider-color`, `--global-text-color-light`.
- Produces: markup `.col-sm-3.abbr` (thumbnail), `.col-sm-9` (text), `div.award-line`, `span.cited-by`; check group `pubs`.

- [ ] **Step 1: Add the `pubs` check group (failing test)**

In `bin/check_redesign.py` add above `GROUPS = {`:

```python
def check_pubs():
    html = read_site("publications/index.html")
    titles = html.count('<div class="title">')
    expect(titles == bib_entries(), f"publications page shows {titles} papers, papers.bib has {bib_entries()}")
    awards = html.count('class="award-line"')
    award_entries = bib_count(r"^\s*award\s*=")
    expect(awards == award_entries, f"publications page shows {awards} award lines, papers.bib has {award_entries}")
    expect('class="award btn' not in html, "collapsible award button still rendered")
    expect('class="award hidden' not in html, "hidden award block still rendered")
    expect("preview z-depth-1" not in html, "paper thumbnails still have the z-depth-1 shadow")
    expect("col-sm-3 abbr" in html, "thumbnail column is not col-sm-3")
    expect("img.shields.io/badge/scholar" not in html, "Scholar citation badge image still used")
    css = read_site("assets/css/main.css")
    expect(".award-line" in css, "main.css has no .award-line rule")
```

and add `"pubs": check_pubs,` to `GROUPS`.

Run: `python3 bin/check_redesign.py pubs`
Expected: `[FAIL] pubs` (0 award lines vs 2, award button and hidden block present, z-depth-1 present, column not col-sm-3, no `.award-line`). The title count already passes (33).

- [ ] **Step 2: Edit `_layouts/bib.liquid`**

1. `<div class="col col-sm-2 abbr">` → `<div class="col-sm-3 abbr">`
2. Both `class="preview z-depth-1 rounded"` (the `<img>` for remote previews and the `figure.liquid` include) → `class="preview rounded"`
3. `class="{% if site.enable_publication_thumbnails %}col-sm-8{% else %}col-sm-10{% endif %}"` → `class="{% if site.enable_publication_thumbnails %}col-sm-9{% else %}col-sm-12{% endif %}"`
4. Delete the award button at the top of `<div class="links">`:

```liquid
{% if entry.award %}
  <a class="award btn btn-sm z-depth-0" role="button">
    {%- if entry.award_name %}{{ entry.award_name }}{% else %}Awarded{% endif -%}
  </a>
{% endif %}
```

5. Directly after the second `<div class="periodical">…{{ entry.note | strip }}…</div>` and before `<!-- Links/Buttons -->`, insert:

```liquid
{% if entry.award %}
  <div class="award-line">
    🏆
    {% if entry.award_name %}{{ entry.award_name }}: {% endif -%}
    {{ entry.award | markdownify | remove: '<p>' | remove: '</p>' | strip }}
  </div>
{% endif %}
```

6. In the Google Scholar badge, replace

```liquid
<img
  src="https://img.shields.io/badge/scholar-{{ citation_count }}-4285F4?logo=googlescholar&labelColor=beige"
  alt="{{ citation_count }} Google Scholar citations"
>
```

with

```liquid
<span class="cited-by">Cited by {{ citation_count }}</span>
```

7. Delete the hidden award block near the end:

```liquid
{% if entry.award %}
  <!-- Hidden Award block -->
  <div class="award hidden d-print-inline">
    <p>{{ entry.award | markdownify }}</p>
  </div>
{% endif %}
```

- [ ] **Step 3: Replace `_sass/_publications.scss`**

```scss
/*******************************************************************************
 * Publication and bibliography styles
 ******************************************************************************/

@use "variables" as v;

.publications {
  margin-top: 2rem;

  h1 {
    color: var(--global-theme-color);
    font-size: 2rem;
    text-align: center;
    margin-top: 1em;
    margin-bottom: 1em;
  }

  h2 {
    margin-bottom: 1rem;

    span {
      font-size: 1.5rem;
    }
  }

  // Year headings on /publications/
  h2.bibliography {
    color: var(--global-heading-color);
    font-size: 1.4rem;
    text-align: left;
    border-top: 0;
    border-bottom: 1px solid var(--global-divider-color);
    padding-top: 0;
    padding-bottom: 0.35rem;
    margin-top: 2.5rem;
  }

  ol.bibliography {
    list-style: none;
    padding: 0;
    margin-top: 0;

    li {
      margin-bottom: 0;
      padding: 1rem 0;

      & + li {
        border-top: 1px solid var(--global-divider-color);
      }

      .preview {
        display: inline-block;
        width: 100%;
        border-radius: 6px !important;
      }

      .abbr {
        margin-bottom: 0.5rem;

        abbr {
          display: inline-block;
          background-color: var(--global-theme-color);
          margin-bottom: 0.5rem;
          color: var(--global-card-bg-color) !important;

          a {
            color: white;

            &:hover {
              text-decoration: none;
            }
          }
        }
      }

      .title {
        font-weight: 600;
        color: var(--global-theme-color);
        line-height: 1.35;
        margin-bottom: 0.15rem;
      }

      .author {
        font-size: 0.93rem;

        a {
          border-bottom: 1px dashed var(--global-theme-color);

          &:hover {
            border-bottom-style: solid;
            text-decoration: none;
          }
        }

        // the site owner's name
        > em {
          font-style: normal;
          font-weight: 700;
        }

        > span.more-authors {
          color: var(--global-text-color-light);
          border-bottom: 1px dashed var(--global-text-color-light);
          cursor: pointer;

          &:hover {
            color: var(--global-text-color);
            border-bottom: 1px dashed var(--global-text-color);
          }
        }
      }

      .periodical {
        font-size: 0.93rem;
        color: var(--global-text-color-light);
      }

      .award-line {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--global-award-color);
        margin-top: 0.2rem;
      }

      .links {
        margin-top: 0.25rem;

        a.btn {
          color: var(--global-theme-color);
          border: 0;
          box-shadow: none;
          padding: 0;
          margin: 0 0.6rem 0 0;
          font-size: 0.85rem;
          text-transform: none;
          letter-spacing: 0;

          &::before {
            content: "[";
          }

          &::after {
            content: "]";
          }

          &:hover {
            color: var(--global-hover-color);
            text-decoration: underline;
          }
        }
      }

      .badges {
        padding-bottom: 0.5rem;

        span {
          display: inline-block;
          color: v.$black-color;
          height: 100%;
          padding-right: 0.5rem;
          vertical-align: middle;

          &:hover {
            text-decoration: underline;
          }
        }

        .cited-by {
          color: var(--global-text-color-light);
          font-size: 0.85rem;
        }
      }

      .hidden {
        font-size: 0.875rem;
        max-height: 0px;
        overflow: hidden;
        text-align: justify;
        transition: all 0.15s ease;

        p {
          line-height: 1.4em;
          margin: 10px;
        }

        pre {
          font-size: 1em;
          line-height: 1.4em;
          padding: 10px;
        }
      }

      .hidden.open {
        max-height: 100em;
        transition: all 0.15s ease;
      }

      div.abstract.hidden {
        border: dashed 1px var(--global-bg-color);
      }

      div.abstract.hidden.open {
        border-color: var(--global-text-color);
      }
    }
  }
}

.citation,
.citation-number {
  color: var(--global-theme-color);
}
```

(The bib search input keeps its existing plain style from `_utilities.scss`; it already is a single text field, so nothing to change.)

- [ ] **Step 4: Rebuild and verify**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py tokens nav home sections pubs links`
Expected: all `[PASS]` (33 papers, 2 award lines; homepage still 5 selected papers).

- [ ] **Step 5: Screenshots**

Run: `bin/shoot_pages.sh "$SHOTS/5-pubs"`. Pass criteria for `publications-desktop-light.png` / `-dark.png`: year headings in serif on the left with a hairline; thumbnail left (no shadow), blue bold title, "Peiran Wang" bold (not underlined, not italic), muted venue line, `[Bib] [HTML]` text links; Moderator (2024) and FLPhish (2021) show a gold "🏆 …" line (dark gold on white, gold on navy). Clicking behavior of `[Bib]` / `[Abs]` is unchanged (spot-check in a browser at <http://localhost:8080/publications/>).

- [ ] **Step 6: Format and commit**

```bash
npx prettier --write --ignore-unknown _layouts/bib.liquid _sass/_publications.scss
git add _layouts/bib.liquid _sass/_publications.scss bin/check_redesign.py
git commit -F - <<'EOF'
style: Restyle paper list with inline award line and text links

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

---

### Task 6: Other pages, footer, and production parity

**Files:**

- Modify: `_pages/research.md` (figure classes only), `_pages/news.md` (`title`), `_sass/_ucla.scss` (append), `_sass/_footer.scss`, `_config.yml` (`footer_fixed`, `last_updated`), `bin/check_redesign.py`

**Interfaces:**

- Consumes: everything above.
- Produces: check group `pages`; final verified branch.

- [ ] **Step 1: Add the `pages` check group (failing test)**

In `bin/check_redesign.py` add above `GROUPS = {`:

```python
def check_pages():
    for page in (
        "index.html",
        "publications/index.html",
        "research/index.html",
        "news/index.html",
        "blog/index.html",
        "cv/index.html",
        "404.html",
    ):
        html = read_site(page)
        expect('class="fixed-bottom"' not in html, f"{page}: footer is still fixed")
        expect("Last updated" in html, f"{page}: footer has no 'Last updated'")
    research = between(read_site("research/index.html"), "<article", "</article>")
    expect("z-depth-1" not in research, "research figures still use z-depth-1 shadows")
    news = read_site("news/index.html")
    expect(re.search(r'<h1 class="post-title">\s*News\s*</h1>', news) is not None, "news page title is not 'News'")
```

and add `"pages": check_pages,` to `GROUPS`.

Run: `python3 bin/check_redesign.py pages`
Expected: `[FAIL] pages` (fixed footer on all 7 pages, no "Last updated", research shadows, title "news").

- [ ] **Step 2: Content-page tweaks**

```bash
sed -i '' 's/class="img-fluid rounded z-depth-1"/class="img-fluid rounded"/' _pages/research.md
grep -c 'z-depth-1' _pages/research.md   # expect 0
```

`_pages/news.md`: `title: news` → `title: News`.

Append to `_sass/_ucla.scss`:

```scss
// Figures in pages and posts: 8px corners, no heavy shadow
.post figure img.rounded {
  border-radius: 8px !important;
}
```

- [ ] **Step 3: Footer**

`_config.yml`: `footer_fixed: true` → `footer_fixed: false`; `last_updated: false # …` → `last_updated: true # …` (keep the comment).

In `_sass/_footer.scss` replace the `footer.sticky-bottom { … }` rule with:

```scss
footer.sticky-bottom {
  border-top: 1px solid var(--global-divider-color);
  padding-top: 1.25rem;
  padding-bottom: 2rem;
  font-size: 0.8rem;

  .container {
    text-align: center;
    color: var(--global-text-color-light);
  }
}
```

- [ ] **Step 4: Rebuild and verify everything**

Run: `bin/wait_for_build.sh && python3 bin/check_redesign.py all`
Expected: `[PASS]` for tokens, links, nav, home, sections, pubs, pages.

- [ ] **Step 5: Full screenshot review**

Run: `bin/shoot_pages.sh "$SHOTS/6-final"` (28 images). Pass criteria per page, light and dark, desktop and phone: consistent navbar; serif page titles capitalized (Publications, Research, News, Blog, CV); Research figures have rounded corners and no heavy shadow; CV page icons and PDF icon in UCLA blue; 404 page readable; footer is a small muted centered line after the content with "Last updated"; nothing overflows horizontally on phones.

- [ ] **Step 6: Production parity (Review Focus 1)**

```bash
docker compose down
docker compose run --rm -e JEKYLL_ENV=production jekyll bundle exec jekyll build
npx -y purgecss -c purgecss.config.js
python3 bin/check_redesign.py tokens nav pubs links
python3 -m http.server 8090 -d _site >/dev/null 2>&1 &
bin/shoot_pages.sh "$SHOTS/6-production" http://localhost:8090
kill %1
docker compose up -d && bin/wait_for_build.sh
```

Expected: the four groups `[PASS]` on the purged production CSS; `$SHOTS/6-production/home-desktop-light.png` and `-dark.png` match `$SHOTS/6-final` (gold section rules, UCLA box, award line, dark tokens all present). If a check fails only in production, diff the minified HTML against the dev build before concluding a style was purged.

- [ ] **Step 7: Format and commit**

```bash
npx prettier --write --ignore-unknown _pages/research.md _pages/news.md _sass/_ucla.scss _sass/_footer.scss _config.yml
git add _pages/research.md _pages/news.md _sass/_ucla.scss _sass/_footer.scss _config.yml bin/check_redesign.py
git commit -F - <<'EOF'
style: Light end-of-page footer, flat research figures, capitalized News title

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
EOF
```

- [ ] **Step 8: Hand-off summary**

Report to the user: branch `ucla-redesign` commits, `python3 bin/check_redesign.py all` output, the path of `$SHOTS/6-final`, and these pre-existing items left untouched: CV page PDF icon points to `example_pdf.pdf` and its description is template text (`_pages/cv.md`); 8 known broken links (blog template tags/categories, `people` page); no paper has `google_scholar_id`, so "Cited by N" does not show yet; 14 files not Prettier-formatted before this work.
