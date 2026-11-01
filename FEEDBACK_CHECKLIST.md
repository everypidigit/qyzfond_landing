# Final feedback package — 1 November 2026

Source: “Сайт QYZfond — финальный пакет правок.docx”. Approved translations are stored in `static/data/site-content.json`. Internal handover checklist; this file is not included in the exported website.

## 1. Technical and structural changes

- [x] 1.1: Dedicated RU/KZ/EN pages, language-preserving internal links and language switching. Existing `?lang=en`, `?lang=kk` and `?lang=kz` links also work. Saved language is used when entering through the unlocalized root.
- [x] 1.2: Gala, all five programs, safeguarding, notice and public offer rendered in three languages.
- [x] 1.3: Homepage about, SDGs, trustees, team, event date, tracks, statistics, donation details and partner headings translated.
- [x] 1.4: Localized titles, descriptions, canonical and alternate URLs; absolute JPEG social-preview URL, Open Graph and Twitter metadata. Share `/ru/`, `/kk/` or `/en/` for a preview in the intended language.
- [x] 1.5: Standalone profidence page removed from routes, export and sitemap; mentions in about/program introduction retained.
- [x] 1.6: Homepage order and section numbers match the document. Gallery follows programs; continuity text begins history; team follows history.
- [x] 1.7: Board of Trustees centered.
- [x] 1.8: Ideathon button still points to qyzfond.org. The event site must receive its own URL before this foundation site replaces it there.
- [x] 1.9: English “Learn more →”, full legal footer with BIN and both Instagram links added.

## 2–3. Brand, homepage and team

- [x] Official foundation names, exact slogans and title/description translations from the document.
- [x] 3.1: New hero copy; a single small rebrand note; continuity block moved to history.
- [x] 3.2: Approved about text; official UN SDG SVGs for 3/4/5/8/10, English on EN and Russian on RU/KZ, UN link and translated disclaimer.
- [x] 3.3: Existing team ordered as requested; translated names/roles; Zhanel's Kazakh-language Kumbel LAB role; Олеся spelling; corrected chair's LinkedIn profile.
- [x] New coordinator cards omitted for now at the user's explicit request on 1 November. Alejandra and Gaukhar are not published with incomplete names or placeholder portraits.
- [x] 3.4: Revised timeline with 2018 and 2021 entries, Ö spelling, 25+ label, program archive below the timeline.
- [x] 3.5: 2026 report is non-clickable and labeled “in preparation” in each language; 2024/2025 keep the same auditor PDF.
- [x] 3.6: Halyk and Kaspi contribution links, bank details and public offer link in three languages. No Freedom Bank button.
- [x] 3.7: All partner headings translated.
- [x] 3.8: Both foundation and student-community Instagram links in contacts and footer.
- [x] 3.9: Gallery “Practice” caption translated; program names retained.

## 4. Ideathon by QYZfond

- [x] Past-tense approved text, consistent event name, 882 registered students / 56 colleges / 172 projects / 10 tracks, acknowledgments and ten translated tracks.
- [x] Old video removed; no outdated video presented as a final-results video.
- [ ] Final video URLs — awaiting the foundation's links via the user.

## 5. AVANTI gala

- [x] Homepage registration and details links, translated date and location.
- [x] Event block and navigation automatically hidden from 14 November 2026, Almaty time. Server rendering and static-site browser logic both enforce the cutoff.
- [x] Approved three-language copy, fund-program cover photo, compact program/menu layout.
- [x] Registration form, 50,000 ₸ individual contribution, corporate contribution formats, Halyk/Kaspi and partnership email.
- [x] No ticket/price wording and no telephone link on the gala page.
- [x] Private partner presentation link and PDF removed from the site. The old PDF remains recoverable through Git history.
- [ ] Photos from the 13 November gala — foundation will supply these after the event; no past-gala gallery is shown.

## 6. Programs

- [x] 6.1: Common labels, outcomes, participation links and back links translated.
- [x] 6.2: College-teacher question updated; Mayak PRO added fourth with purple accent, published logo and photo from kazfond.kz. Five programs in the requested order.
- [x] 6.3: Kumbel LAB — all approved fields on RU/KZ/EN pages.
- [x] 6.4: Impactum! — running since 2018; new cohort from October 2026; all approved translations.
- [x] 6.5: Kumbel PRO — launched 2018; Ustaz PRO accreditation; all approved translations.
- [x] 6.6: Mayak PRO — new localized page with approved audience, format, curriculum and mentoring outcomes.
- [x] 6.7: Örkendarium — 2026 results, childcare and two four-week levels, award/support text, direct program-site/application link.
- [x] 6.8: Three compact archive cards with original Kumbel/Mayak/Mira logos, years, slogans and approved descriptions. No new archive pages.

## 7. Documents

- [x] 7.1: Existing published safeguarding and ethics PDFs downloaded in RU/KZ/EN; published form links retained, including the English participant form.
- [x] 7.2: Approved fraud notice in three languages.
- [x] 7.3: Original published public offers imported from kazfond.kz in all three languages, without new translation or rewriting. No fallback notice is needed.

## Verification

- [x] Python integration suite: all translated routes, language aliases, internal navigation, homepage order, approved program results, donation/form links, legal PDF selection and removed pages/assets.
- [x] Chromium: 105 route/language/viewport combinations (320, 375, 768, 1024 and 1440 px), no page overflow or wrapped/clipped program headings.
- [x] Browser navigation: EN share link → EN program → KZ switch on the same program → saved KZ at root.
- [x] Export: all 41 generated HTML documents checked for local assets, internal destinations and absolute social-preview metadata.

## Source assets

- SDG icons: `https://kazakhstan.un.org/profiles/undg_country/themes/custom/undg/images/SDGs/{ru|en}/SDG-{n}.svg`.
- Mayak PRO logo/photo: foundation's published `/ru/projects-majak-pro/` page; full-resolution photo used where available.
- Archive logos: foundation's original published program assets.
- Public offers: `/ru/oferta/`, `/kk/oferta-3/`, `/en/oferta-2/` on kazfond.kz.
- Safeguarding/ethics: language-specific links on the foundation's published safeguarding pages.
- Hero, gallery and existing portraits: previously approved user-supplied assets; retained.
