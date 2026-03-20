# Migrate Academic Website Content Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate Peiran Wang's former academic homepage (AcadHomepage theme) content into the new al-folio project, with separate commits per logical content area.

**Architecture:** The former site uses a single `about.md` page with all content inline. Al-folio uses structured data files (YAML, BibTeX), separate page files, and collection directories. Each content area (config, about, news, publications, CV, assets) maps to specific al-folio files.

**Tech Stack:** Jekyll, YAML, BibTeX, Markdown, Liquid templates

---

## File Structure

| Content Area | Former Source | Al-folio Target |
|---|---|---|
| Site config & personal info | `_config.yml` | `_config.yml` |
| Social links | `_config.yml` (author section) | `_data/socials.yml` |
| Profile image | `images/img.png` | `assets/img/prof_pic.jpg` |
| CV PDF | `files/CV.pdf` | `assets/pdf/CV.pdf` |
| Transcript | `files/Transcript_peiran.pdf` | `assets/pdf/Transcript_peiran.pdf` |
| About/bio text | `_pages/about.md` | `_pages/about.md` |
| News items | `_pages/about.md` (inline) | `_news/announcement_*.md` (separate files) |
| Publications | `_pages/about.md` (inline) | `_bibliography/papers.bib` |
| Education | `_pages/about.md` (inline) | `_data/cv.yml` |
| Experiences | `_pages/about.md` (inline) | `_data/cv.yml` |
| Honors & Awards | `_pages/about.md` (inline) | `_data/cv.yml` |
| Academic Services | `_pages/about.md` (inline) | `_data/cv.yml` |

---

## Chunk 1: Configuration & Assets

### Task 1: Update _config.yml with personal information

**Files:**
- Modify: `_config.yml`

- [ ] **Step 1: Update site metadata in _config.yml**

Replace the following fields in `_config.yml`:

```yaml
title: WhileBug
first_name: Peiran
middle_name:
last_name: Wang
contact_note: >
  Feel free to reach out via email.
description: >
  A master student from Tsinghua University in system/blockchain/PLSE research.
keywords: blockchain, distributed-system, federated-learning, cybersecurity, PLSE, academic-website
lang: en
```

- [ ] **Step 2: Update Jekyll Scholar author config**

In `_config.yml`, update the `scholar` section:

```yaml
scholar:
  last_name: [Wang]
  first_name: [Peiran, P.]
```

- [ ] **Step 3: Update blog settings**

```yaml
blog_name: WhileBug's Blog
blog_description: Peiran Wang's academic blog
```

- [ ] **Step 4: Remove example external sources**

Clear the `external_sources` section (remove the medium.com and Google Blog entries), set to empty list or remove.

- [ ] **Step 5: Verify _config.yml is valid YAML**

Run: `docker compose run --rm jekyll bundle exec jekyll doctor 2>&1 || echo "Check manually"`
Or simply review the file visually for YAML syntax errors.

- [ ] **Step 6: Commit**

```bash
git add _config.yml
git commit -m "chore: update site config with personal information"
```

---

### Task 2: Update social links

**Files:**
- Modify: `_data/socials.yml`

- [ ] **Step 1: Replace socials.yml content**

```yaml
cv_pdf: /assets/pdf/CV.pdf
email: whilebug@gmail.com
github_username: whilebug
scholar_userid: mHy2_KIAAAAJ
rss_icon: true
```

Remove the `inspirehep_id`, `custom_social`, and example placeholder values.

- [ ] **Step 2: Commit**

```bash
git add _data/socials.yml
git commit -m "chore: update social links with personal accounts"
```

---

### Task 3: Copy profile image and PDF assets

**Files:**
- Copy: `former_website/whilebug.github.io/images/img.png` -> `assets/img/prof_pic.png`
- Copy: `former_website/whilebug.github.io/files/CV.pdf` -> `assets/pdf/CV.pdf`
- Copy: `former_website/whilebug.github.io/files/Transcript_peiran.pdf` -> `assets/pdf/Transcript_peiran.pdf`

- [ ] **Step 1: Copy profile image**

```bash
cp former_website/whilebug.github.io/images/img.png assets/img/prof_pic.jpg
```

- [ ] **Step 2: Copy PDF files**

```bash
cp former_website/whilebug.github.io/files/CV.pdf assets/pdf/CV.pdf
cp former_website/whilebug.github.io/files/Transcript_peiran.pdf assets/pdf/Transcript_peiran.pdf
```

- [ ] **Step 3: Remove old example PDF if it exists**

```bash
rm -f assets/pdf/example_pdf.pdf
```

- [ ] **Step 4: Commit**

```bash
git add assets/img/prof_pic.jpg assets/pdf/CV.pdf assets/pdf/Transcript_peiran.pdf
git rm --cached assets/pdf/example_pdf.pdf 2>/dev/null || true
git commit -m "chore: add profile image and PDF assets"
```

---

## Chunk 2: About Page & News

### Task 4: Update about page

**Files:**
- Modify: `_pages/about.md`

- [ ] **Step 1: Update about.md front matter and content**

Replace the entire `_pages/about.md` with:

```markdown
---
layout: about
title: about
permalink: /
subtitle: Master student at <a href='https://www.tsinghua.edu.cn/en/'>Tsinghua University</a>, Institute of Network Sciences and Cyberspace.

profile:
  align: right
  image: prof_pic.png
  image_circular: false
  more_info: >
    <p>Beijing, China</p>
    <p>whilebug@gmail.com</p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
  scrollable: true
  limit: 3
---

I'm WhileBug (Peiran Wang, 王沛然), a student interested in Blockchain/System/Networking/PLSE. I am pursuing a master's degree in cybersecurity at Tsinghua University. I graduated from Sichuan University Cybersecurity Talented Class in 2022. During my undergraduate studies, I received the National Scholarship and achieved a GPA of 3.92.

I organize [SCU-Leap-Manual](https://scu-cs-runner.github.io/SurviveSCUManual/) for CS/SE/Cybersecurity students at SCU. If you want to join us, please drop me an email.

My research interests include distributed systems, blockchain, AI security/privacy, and PLSE.
```

- [ ] **Step 2: Commit**

```bash
git add _pages/about.md
git commit -m "feat: update about page with personal bio"
```

---

### Task 5: Create news announcements

**Files:**
- Modify: `_news/announcement_1.md`
- Modify: `_news/announcement_2.md`
- Modify: `_news/announcement_3.md`
- Create: `_news/announcement_4.md`
- Create: `_news/announcement_5.md`
- Create: `_news/announcement_6.md`

- [ ] **Step 1: Replace announcement_1.md**

```markdown
---
layout: post
date: 2023-03-15 00:00:00+0800
inline: true
related_posts: false
---

Looking for finance/tech internship in blockchain/system at company during 2023 summer. If you are interested in working with me, please drop me an email.
```

- [ ] **Step 2: Replace announcement_2.md**

```markdown
---
layout: post
date: 2023-03-01 00:00:00+0800
inline: true
related_posts: false
---

Welcome to my new homepage!
```

- [ ] **Step 3: Replace announcement_3.md**

```markdown
---
layout: post
date: 2022-09-01 00:00:00+0800
inline: true
related_posts: false
---

Started pursuing a master's degree at Tsinghua University!
```

- [ ] **Step 4: Create announcement_4.md**

```markdown
---
layout: post
date: 2022-06-20 00:00:00+0800
inline: true
related_posts: false
---

Graduated from Sichuan University with Outstanding Graduate honor and Outstanding Undergraduate Thesis!
```

- [ ] **Step 5: Create announcement_5.md**

```markdown
---
layout: post
date: 2022-06-15 00:00:00+0800
inline: true
related_posts: false
---

Finished research internship at Microsoft Research Asia with MSRA Star of Tomorrow Award!
```

- [ ] **Step 6: Create announcement_6.md**

```markdown
---
layout: post
date: 2021-09-01 00:00:00+0800
inline: true
related_posts: false
---

Started research internship at Microsoft Research Asia, Systems and Networking Research Group.
```

- [ ] **Step 7: Commit**

```bash
git add _news/
git commit -m "feat: add news announcements"
```

---

## Chunk 3: Publications

### Task 6: Create bibliography entries

**Files:**
- Modify: `_bibliography/papers.bib`

- [ ] **Step 1: Replace papers.bib with personal publications**

Replace the entire content of `_bibliography/papers.bib` with:

```bibtex
---
---

% Accepted & Published

@article{wang2023fgcs,
  abbr          = {FGCS},
  bibtex_show   = {true},
  title         = {Defending Byzantine Attacks in Ensemble Federated Learning: A Reputation-based Phishing Approach},
  author        = {Wang, Peiran and Li, Beibei and others},
  journal       = {Future Generation Computer Systems},
  year          = {2023},
  publisher     = {Elsevier},
  selected      = {true}
}

@inproceedings{wang2021flphish,
  abbr          = {ISCC},
  bibtex_show   = {true},
  title         = {FLPhish: Reputation-based Phishing Byzantine Defense in Ensemble Federated Learning},
  author        = {Wang, Peiran and Li, Beibei and others},
  booktitle     = {IEEE Symposium on Computers and Communications (ISCC)},
  year          = {2021},
  organization  = {IEEE},
  award         = {Best Paper Award},
  award_name    = {Best Paper Award},
  selected      = {true}
}

@inproceedings{wang2022fedvanet,
  abbr          = {GlobeCom},
  bibtex_show   = {true},
  title         = {FedVANET: Efficient Federated Learning with Non-IID Data for Vehicular Ad Hoc Networks},
  author        = {Wang, Peiran and others},
  booktitle     = {IEEE Global Communications Conference (GlobeCom)},
  year          = {2022},
  organization  = {IEEE},
  selected      = {true}
}

@inproceedings{wang2021minedetector,
  abbr          = {CSE},
  bibtex_show   = {true},
  title         = {MineDetector: JavaScript Browser-side Cryptomining Detection using Static Methods},
  author        = {Wang, Peiran and others},
  booktitle     = {IEEE International Conference on Computational Science and Engineering (CSE)},
  year          = {2021},
  organization  = {IEEE}
}

@inproceedings{wang2022geolocation,
  abbr          = {GlobeCom},
  bibtex_show   = {true},
  title         = {Top AS Router Geolocation in Databases: Performance and Techniques},
  author        = {Wang, Peiran and others},
  booktitle     = {IEEE Global Communications Conference (GlobeCom)},
  year          = {2022},
  organization  = {IEEE}
}

% In Submission

@article{wang2023tangram,
  abbr          = {ICLR},
  bibtex_show   = {true},
  title         = {TANGRAM: Automating Execution Planning for Distributed Deep Neural Network},
  author        = {Wang, Peiran and others},
  journal       = {In submission to ICLR},
  year          = {2023}
}

@article{wang2023dimtsl,
  abbr          = {NeurIPS},
  bibtex_show   = {true},
  title         = {DimT-SL: Mitigating Label Leakage in Two-Party Split Learning},
  author        = {Wang, Peiran and others},
  journal       = {In submission to NeurIPS},
  year          = {2023}
}

@article{wang2023fedclip,
  abbr          = {IJCAI},
  bibtex_show   = {true},
  title         = {FedCliP: Communication Efficient Federated Learning with Client Pruning},
  author        = {Wang, Peiran and others},
  journal       = {In submission to IJCAI},
  year          = {2023}
}

@article{wang2023fedchain,
  abbr          = {Blockchain},
  bibtex_show   = {true},
  title         = {FedChain: A Secure Proof of Federated Learning Consensus Protocol for Blockchain},
  author        = {Wang, Peiran and others},
  journal       = {In submission},
  year          = {2023}
}

@article{wang2023tinyg,
  abbr          = {CNSM},
  bibtex_show   = {true},
  title         = {TinyG: Accurate IP Geolocation Using a Tiny Number of Probers},
  author        = {Wang, Peiran and others},
  journal       = {In submission to CNSM},
  year          = {2023}
}

@article{wang2023pfedrpca,
  abbr          = {INFOCOM},
  bibtex_show   = {true},
  title         = {pFedRPCA: Personalized Federated Learning with Robust Principal Component Analysis},
  author        = {Wang, Peiran and others},
  journal       = {In submission to INFOCOM},
  year          = {2023}
}

% In Draft

@unpublished{wang2023privacy,
  bibtex_show   = {true},
  title         = {Privacy-Preserving Generative Adversarial Learning},
  author        = {Wang, Peiran and others},
  year          = {2023},
  note          = {In draft}
}

@unpublished{wang2023ethics,
  bibtex_show   = {true},
  title         = {Defending Ethics Risks in Generative Models},
  author        = {Wang, Peiran and others},
  year          = {2023},
  note          = {In draft}
}

@unpublished{wang2023completion,
  bibtex_show   = {true},
  title         = {Defending Model Completion Attack in Split Learning via Dimension Confusion},
  author        = {Wang, Peiran and others},
  year          = {2023},
  note          = {In draft}
}

@unpublished{wang2023sparse,
  bibtex_show   = {true},
  title         = {Personalized Federated Learning via Sparse Local Training},
  author        = {Wang, Peiran and others},
  year          = {2023},
  note          = {In draft}
}
```

**Note:** The `author` fields use `others` as a placeholder. The user should fill in the complete author lists if known. Also, the user may want to add `pdf`, `code`, `html` links to individual entries later.

- [ ] **Step 2: Commit**

```bash
git add _bibliography/papers.bib
git commit -m "feat: add publications bibliography"
```

---

## Chunk 4: CV Data

### Task 7: Update CV data with education, experiences, honors, and services

**Files:**
- Modify: `_data/cv.yml`

- [ ] **Step 1: Replace cv.yml with personal CV data**

Replace the entire content of `_data/cv.yml` with:

```yaml
cv:
  name: Peiran Wang
  label: Master Student
  email: whilebug@gmail.com
  location: Beijing, China
  image: ""
  summary: A master student at Tsinghua University interested in Blockchain, Distributed Systems, AI Security/Privacy, and PLSE.

  social_networks:
    - network: GitHub
      username: whilebug

  address:
    city: Beijing
    countryCode: CN

  sections:
    Education:
      - institution: Tsinghua University
        location: Beijing, China
        url: https://www.tsinghua.edu.cn/en/
        area: Cybersecurity
        studyType: Master
        start_date: 2022-09
        end_date: 2025-04
        highlights:
          - Institute of Network Sciences and Cyberspace

      - institution: Sichuan University
        location: Chengdu, China
        url: https://www.scu.edu.cn/
        area: Cybersecurity
        studyType: Bachelor
        start_date: 2018-09
        end_date: 2022-06
        highlights:
          - "Cybersecurity Excellence Class (Rank: 1/18)"
          - Outstanding Undergraduate
          - Outstanding Undergraduate Thesis

    Experience:
      - company: Johns Hopkins University
        position: Research Collaborator
        location: U.S.
        url: https://yinzhicao.org/
        start_date: 2022-06
        end_date: ""
        summary: Working with Prof. Yinzhi Cao.

      - company: Tsinghua University
        position: Research Assistant
        location: Beijing, China
        start_date: 2022-09
        end_date: 2023-04
        summary: Internet Measurement Group.

      - company: Purdue University
        position: Research Collaborator
        location: U.S.
        url: https://yonglezh-purdue.github.io/
        start_date: 2022-08
        end_date: 2023-03
        summary: Working with Prof. Yongle Zhang.

      - company: Microsoft Research Asia
        position: Research Intern
        location: Beijing, China
        url: https://www.microsoft.com/en-us/research/group/systems-and-networking-research-group-asia/
        start_date: 2021-09
        end_date: 2022-06
        summary: Systems and Networking Research Group.

      - company: Sichuan University
        position: Research Assistant
        location: Chengdu, China
        url: https://li-beibei.github.io/
        start_date: 2020-09
        end_date: 2022-06
        summary: Working with Prof. Beibei Li.

      - company: Sichuan University
        position: Research Assistant
        location: Chengdu, China
        url: https://chenghuang.org/
        start_date: 2020-05
        end_date: 2020-11
        summary: Working with Prof. Cheng Huang.

    Awards:
      - title: Outstanding Undergraduate Thesis
        date: 2022-08
        awarder: Sichuan University

      - title: Microsoft Research Asia Star of Tomorrow Award
        date: 2022-06
        awarder: Microsoft Research Asia

      - title: Outstanding Undergraduate Graduates
        date: 2022-06
        awarder: Sichuan University

      - title: IEEE ISCC 2021 Best Paper Award
        date: 2021-09
        awarder: IEEE ISCC

      - title: National Scholarship (top 0.2% students in China)
        date: 2019-08
        awarder: National Ministry of Education

      - title: First Class Scholarship
        date: 2019-08
        awarder: Sichuan University

    Skills:
      - name: Research Areas
        level: ""
        icon: fa-solid fa-hashtag
        keywords: "Distributed Systems, Blockchain, Federated Learning, AI Security/Privacy, PLSE"

    Volunteer:
      - company: IEEE TIFS
        position: Reviewer
        start_date: ""
        end_date: ""

      - company: IEEE KSEM, IEEE ICC, AAAI
        position: External Reviewer
        start_date: ""
        end_date: ""
```

- [ ] **Step 2: Commit**

```bash
git add _data/cv.yml
git commit -m "feat: update CV with education, experience, and awards"
```

---

## Chunk 5: Cleanup

### Task 8: Clean up example/placeholder content

**Files:**
- Modify: `_data/coauthors.yml` (clear example data or keep empty)
- Modify: `_data/repositories.yml` (update with personal repos)
- Remove: `_pages/about_einstein.md` (if it exists, already excluded in config)

- [ ] **Step 1: Update repositories.yml with personal GitHub info**

Replace content of `_data/repositories.yml`:

```yaml
github_users:
  - whilebug

github_repos: []

repo_description_lines_max: 2
```

- [ ] **Step 2: Clear example coauthors data**

Replace `_data/coauthors.yml` with an empty file or minimal content:

```yaml
# Coauthors data
# Add coauthor information here
# See: https://github.com/alshedivat/al-folio#coauthors
```

- [ ] **Step 3: Remove example news files content (already replaced in Task 5)**

Verify the news files from Task 5 are correct.

- [ ] **Step 4: Commit**

```bash
git add _data/coauthors.yml _data/repositories.yml
git commit -m "chore: clean up example placeholder content"
```

---

## Commit Summary

| Commit # | Message | Content |
|---|---|---|
| 1 | `chore: update site config with personal information` | _config.yml |
| 2 | `chore: update social links with personal accounts` | _data/socials.yml |
| 3 | `chore: add profile image and PDF assets` | prof_pic.png, CV.pdf, Transcript.pdf |
| 4 | `feat: update about page with personal bio` | _pages/about.md |
| 5 | `feat: add news announcements` | _news/*.md |
| 6 | `feat: add publications bibliography` | _bibliography/papers.bib |
| 7 | `feat: update CV with education, experience, and awards` | _data/cv.yml |
| 8 | `chore: clean up example placeholder content` | _data/coauthors.yml, _data/repositories.yml |

## Notes for the implementer

1. **Publications:** The BibTeX entries use `others` as a placeholder for co-authors. The user should update these with full author lists. Also consider adding `pdf`, `code`, `html`, and `abstract` fields to individual entries.
2. **Profile image:** The former site uses `img.png` (PNG). Al-folio references it as `prof_pic.jpg` by default, but the about.md front matter has been updated to `prof_pic.png` to match.
3. **Google Scholar:** The scholar user ID `mHy2_KIAAAAJ` has been configured in socials.yml.
4. **Friends section:** Not directly supported by al-folio. Could be added as a custom page later if desired.
5. **Invited Talks:** Was empty in the former site, skipped for now.
