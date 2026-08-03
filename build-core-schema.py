#!/usr/bin/env python3
"""
Inject the two structured-data blocks the audit found missing:

  index.html  -- had NO JSON-LD at all. The homepage is the anchor of the
                 entity graph: 830 nodes across the site reference
                 https://www.wasatchfai.com/#clinic, and nothing defined it.
  staff.html  -- had NO JSON-LD, and the site had no Person/Physician entity
                 anywhere. All 123 blog posts credit an organisation as author,
                 which is the single largest E-E-A-T liability on a YMYL
                 medical site. These nodes give those posts real humans to
                 point at.

Every claim below is taken from what staff.html already says in prose. Nothing
is invented -- no NPI numbers, no ratings, no review counts.

Idempotent: re-running replaces the managed block rather than appending.
Run from the repo root.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BASE = "https://www.wasatchfai.com"
MARK_OPEN = "<!-- JSON-LD: managed by build-core-schema.py -->"
MARK_CLOSE = "<!-- /JSON-LD -->"

PHYSICIANS = [
    {
        "id": "dr-campbell", "name": "Jason Campbell",
        "creds": "DPM, MHA, AACFAS",
        "focus": ["Foot and ankle reconstruction", "Sports injuries",
                  "Ankle arthroscopy", "Wound care"],
        # AACFAS = Associate, American College of Foot and Ankle Surgeons
        "college": "Associate of the American College of Foot and Ankle Surgeons",
    },
    {
        "id": "dr-frost", "name": "Colby Frost",
        "creds": "DPM, MHA, FACFAS",
        "focus": ["Complex foot and ankle reconstruction", "Limb salvage",
                  "Pediatric foot deformities"],
        "college": "Fellow of the American College of Foot and Ankle Surgeons",
    },
    {
        "id": "dr-woolley", "name": "Mark Woolley",
        "creds": "DPM, FACFAS",
        "focus": ["Lower-extremity nerve surgery", "Minimally invasive surgery",
                  "Sports medicine"],
        "college": "Fellow of the American College of Foot and Ankle Surgeons",
    },
    {
        "id": "dr-murrah", "name": "Chantel Murrah",
        "creds": "DPM, MHA, MPH, MBA, PhD",
        "focus": ["Non-surgical foot and ankle care", "Diabetic foot care"],
        "college": None,
        "languages": ["English", "Spanish"],
    },
]


def physician_node(p):
    creds = [
        '{ "@type": "EducationalOccupationalCredential", "credentialCategory": "degree",'
        ' "name": "Doctor of Podiatric Medicine (DPM)" }'
    ]
    if p.get("college"):
        creds.append(
            '{ "@type": "EducationalOccupationalCredential",'
            ' "credentialCategory": "professional certification",'
            f' "name": "{p["college"]}",'
            ' "recognizedBy": { "@type": "Organization",'
            ' "name": "American College of Foot and Ankle Surgeons" } }'
        )
    langs = ""
    if p.get("languages"):
        langs = ',\n      "knowsLanguage": [' + ", ".join(f'"{l}"' for l in p["languages"]) + "]"
    focus = ", ".join(f'"{f}"' for f in p["focus"])
    return f"""    {{
      "@type": "Person",
      "@id": "{BASE}/staff.html#{p['id']}",
      "name": "{p['name']}, {p['creds']}",
      "givenName": "{p['name'].split()[0]}",
      "familyName": "{p['name'].split()[-1]}",
      "honorificPrefix": "Dr.",
      "honorificSuffix": "{p['creds']}",
      "jobTitle": "Podiatrist",
      "hasOccupation": {{
        "@type": "Occupation",
        "name": "Podiatrist",
        "occupationalCategory": "29-1081.00"
      }},
      "worksFor": {{ "@id": "{BASE}/#clinic" }},
      "url": "{BASE}/staff.html#{p['id']}",
      "alumniOf": [
        {{ "@type": "CollegeOrUniversity", "name": "Weber State University" }},
        {{ "@type": "CollegeOrUniversity", "name": "Des Moines University" }}
      ],
      "hasCredential": [
{chr(10).join('        ' + c + (',' if i < len(creds) - 1 else '') for i, c in enumerate(creds))}
      ],
      "knowsAbout": [{focus}]{langs}
    }}"""


EMPLOYEE_REFS = ",\n".join(
    f'        {{ "@id": "{BASE}/staff.html#{p["id"]}" }}' for p in PHYSICIANS)

CLINIC_CORE = f"""    {{
      "@type": ["MedicalClinic", "MedicalBusiness"],
      "@id": "{BASE}/#clinic",
      "name": "Wasatch Foot & Ankle Institute",
      "alternateName": "Wasatch FAI",
      "url": "{BASE}/",
      "logo": "{BASE}/images/logo-full.png",
      "image": "{BASE}/images/logo-full.png",
      "email": "contactus@wasatchfai.com",
      "medicalSpecialty": "Podiatric",
      "priceRange": "$$",
      "currenciesAccepted": "USD",
      "paymentAccepted": "Cash, Check, Credit Card, Insurance",
      "description": "Board-certified podiatry and foot & ankle care serving Northern Utah from clinics in Farmington and South Ogden.",
      "areaServed": [
        {{ "@type": "AdministrativeArea", "name": "Davis County, Utah" }},
        {{ "@type": "AdministrativeArea", "name": "Weber County, Utah" }}
      ],
      "employee": [
{EMPLOYEE_REFS}
      ],
      "department": [
        {{ "@id": "{BASE}/farmington-utah.html#clinic" }},
        {{ "@id": "{BASE}/ogden-utah-foot-doctor.html#clinic" }}
      ],
      "openingHoursSpecification": [
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "08:00", "closes": "17:00" }},
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "12:00" }}
      ]
    }}"""

FARMINGTON_NODE = f"""    {{
      "@type": "MedicalClinic",
      "@id": "{BASE}/farmington-utah.html#clinic",
      "name": "Wasatch Foot & Ankle Institute — Farmington",
      "url": "{BASE}/farmington-utah.html",
      "telephone": "+1-801-451-7500",
      "faxNumber": "+1-801-451-6966",
      "email": "contactus@wasatchfai.com",
      "medicalSpecialty": "Podiatric",
      "priceRange": "$$",
      "parentOrganization": {{ "@id": "{BASE}/#clinic" }},
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "473 W. Bourne Circle, Suite 2",
        "addressLocality": "Farmington",
        "addressRegion": "UT",
        "postalCode": "84025",
        "addressCountry": "US"
      }},
      "geo": {{ "@type": "GeoCoordinates", "latitude": 40.9869, "longitude": -111.9066 }},
      "hasMap": "https://www.google.com/maps?q=473+W+Bourne+Circle+Suite+2+Farmington+UT+84025",
      "openingHoursSpecification": [
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "08:00", "closes": "17:00" }},
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "12:00" }}
      ]
    }}"""

OGDEN_NODE = f"""    {{
      "@type": "MedicalClinic",
      "@id": "{BASE}/ogden-utah-foot-doctor.html#clinic",
      "name": "Wasatch Foot & Ankle Institute — South Ogden",
      "url": "{BASE}/ogden-utah-foot-doctor.html",
      "telephone": "+1-801-627-2122",
      "faxNumber": "+1-801-627-2125",
      "email": "contactus@wasatchfai.com",
      "medicalSpecialty": "Podiatric",
      "priceRange": "$$",
      "parentOrganization": {{ "@id": "{BASE}/#clinic" }},
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "945 Chambers Street, Suite 3",
        "addressLocality": "South Ogden",
        "addressRegion": "UT",
        "postalCode": "84403",
        "addressCountry": "US"
      }},
      "geo": {{ "@type": "GeoCoordinates", "latitude": 41.1725, "longitude": -111.9580 }},
      "hasMap": "https://www.google.com/maps?q=945+Chambers+Street+Suite+3+South+Ogden+UT+84403",
      "openingHoursSpecification": [
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "08:00", "closes": "17:00" }},
        {{ "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "12:00" }}
      ]
    }}"""

WEBSITE_NODE = f"""    {{
      "@type": "WebSite",
      "@id": "{BASE}/#website",
      "url": "{BASE}/",
      "name": "Wasatch Foot & Ankle Institute",
      "inLanguage": "en-US",
      "publisher": {{ "@id": "{BASE}/#clinic" }}
    }}"""

INDEX_GRAPH = f"""{MARK_OPEN}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
{WEBSITE_NODE},
    {{
      "@type": "WebPage",
      "@id": "{BASE}/#webpage",
      "url": "{BASE}/",
      "name": "Wasatch Foot & Ankle Institute | Podiatry in Farmington & South Ogden, UT",
      "description": "Warm, expert foot & ankle care in Farmington and South Ogden, Utah.",
      "inLanguage": "en-US",
      "isPartOf": {{ "@id": "{BASE}/#website" }},
      "about": {{ "@id": "{BASE}/#clinic" }}
    }},
{CLINIC_CORE},
{FARMINGTON_NODE},
{OGDEN_NODE}
  ]
}}
</script>
{MARK_CLOSE}"""

STAFF_GRAPH = f"""{MARK_OPEN}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "@id": "{BASE}/staff.html#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Our Physicians", "item": "{BASE}/staff.html" }}
      ]
    }},
    {{
      "@type": "AboutPage",
      "@id": "{BASE}/staff.html#webpage",
      "url": "{BASE}/staff.html",
      "name": "Our Physicians | Wasatch Foot & Ankle Institute",
      "inLanguage": "en-US",
      "isPartOf": {{ "@id": "{BASE}/#website" }},
      "about": {{ "@id": "{BASE}/#clinic" }},
      "mainEntity": {{ "@id": "{BASE}/#clinic" }}
    }},
{",".join(chr(10) + physician_node(p) for p in PHYSICIANS)}
  ]
}}
</script>
{MARK_CLOSE}"""


def inject(filename, block):
    p = ROOT / filename
    s = p.read_text(encoding="utf-8")
    # idempotent: drop any previously managed block
    s = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE), "", s, flags=re.S).rstrip()
    anchor = '<script src="js/site.js" defer></script>'
    if anchor not in s:
        raise SystemExit(f"{filename}: could not find the js/site.js anchor")
    s = s.replace(anchor, block + "\n\n" + anchor, 1)
    p.write_text(s, encoding="utf-8")
    print(f"injected schema into {filename}")


if __name__ == "__main__":
    inject("index.html", INDEX_GRAPH)
    inject("staff.html", STAFF_GRAPH)
