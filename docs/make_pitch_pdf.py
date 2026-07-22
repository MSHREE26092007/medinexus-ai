"""Generate the PEC Hacks 4.0 submission PDF for MediNexus AI.

Mirrors the 7-slide template structure of PecHacks4.0.pptx.
Run: python make_pitch_pdf.py
"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = landscape(A4)

SLATE = HexColor("#0f172a")
SLATE_600 = HexColor("#475569")
SLATE_400 = HexColor("#94a3b8")
TEAL = HexColor("#14b8a6")
TEAL_DARK = HexColor("#0f766e")
LIGHT = HexColor("#f1f5f9")
AMBER = HexColor("#f59e0b")
ROSE = HexColor("#e11d48")

OUT = r"C:\Users\mshre\Downloads\PecHacks4.0_MediNexus_AI.pdf"

c = canvas.Canvas(OUT, pagesize=(W, H))
page_no = 0


def wrap_text(text, font, size, max_w):
    return simpleSplit(text, font, size, max_w)


def draw_par(x, y, text, font="Helvetica", size=11, leading=15,
             color=SLATE_600, max_w=W - 60 * mm):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, max_w):
        c.drawString(x, y, line)
        y -= leading
    return y


def header(title):
    global page_no
    page_no += 1
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(25 * mm, H - 25 * mm, title)
    c.setFillColor(TEAL)
    c.rect(25 * mm, H - 28 * mm, 30 * mm, 1.2 * mm, fill=1, stroke=0)
    # footer
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE_400)
    c.drawString(25 * mm, 10 * mm, "PEC Hacks 4.0  |  MediNexus AI — Autonomous Offline Clinical Intelligence Platform")
    c.drawRightString(W - 25 * mm, 10 * mm, f"{page_no} / 7")


def card(x, y, w, h, fill=LIGHT, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=1 if stroke else 0)


# ---------------- Slide 1 — Title ----------------
page_no += 1
c.setFillColor(SLATE)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(TEAL)
c.rect(0, 0, W, 4 * mm, fill=1, stroke=0)

c.setFillColor(TEAL)
c.roundRect(W / 2 - 12 * mm, H - 62 * mm, 24 * mm, 24 * mm, 5 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 40)
c.drawCentredString(W / 2, H - 55 * mm, "M")

c.setFont("Helvetica-Bold", 15)
c.setFillColor(TEAL)
c.drawCentredString(W / 2, H - 75 * mm, "TEAM MEDINEXUS")

c.setFont("Helvetica-Bold", 34)
c.setFillColor(white)
c.drawCentredString(W / 2, H - 92 * mm, "MediNexus AI")
c.setFont("Helvetica", 16)
c.setFillColor(SLATE_400)
c.drawCentredString(W / 2, H - 102 * mm, "Autonomous Offline Clinical Intelligence Platform")

c.setFillColor(TEAL_DARK)
c.roundRect(W / 2 - 32 * mm, H - 122 * mm, 64 * mm, 10 * mm, 5 * mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(W / 2, H - 118.5 * mm, "Problem Domain: Healthcare")

c.setFont("Helvetica-Bold", 12)
c.setFillColor(TEAL)
demo_txt = "Live demo: mshree26092007.github.io/medinexus-ai"
c.drawCentredString(W / 2, 38 * mm, demo_txt)
tw = c.stringWidth(demo_txt, "Helvetica-Bold", 12)
c.linkURL("https://mshree26092007.github.io/medinexus-ai/",
          (W / 2 - tw / 2, 36 * mm, W / 2 + tw / 2, 43 * mm), relative=0)

repo_txt = "GitHub: github.com/MSHREE26092007/medinexus-ai"
c.drawCentredString(W / 2, 31 * mm, repo_txt)
tw = c.stringWidth(repo_txt, "Helvetica-Bold", 12)
c.linkURL("https://github.com/MSHREE26092007/medinexus-ai",
          (W / 2 - tw / 2, 29 * mm, W / 2 + tw / 2, 36 * mm), relative=0)

c.setFont("Helvetica", 10)
c.setFillColor(SLATE_400)
c.drawCentredString(W / 2, 22 * mm,
                    "VIT Chennai  x  Easwari Engineering College  x  Sri Venkateswara College of Engineering")
c.showPage()

# ---------------- Slide 2 — Problem Statement ----------------
header("Problem Statement")
y = H - 45 * mm
paras = [
    "In rural clinics, small hospitals, and disaster or low-connectivity zones, clinicians work without the "
    "AI-powered decision support that urban hospitals increasingly rely on — because nearly every clinical AI "
    "tool today is cloud-dependent. No internet means no intelligence.",
    "Patient information is fragmented across paper files and disconnected spreadsheets, so deterioration "
    "often goes unnoticed until it becomes an emergency. Overloaded doctors spend up to a third of their time "
    "on manual documentation instead of patient care, and referring to medical literature mid-consultation is "
    "impractical under time pressure.",
    "Cloud AI also raises a hard barrier: sending sensitive patient records to third-party servers creates "
    "privacy, compliance, and cost problems that many institutions in developing regions simply cannot accept.",
]
for ptext in paras:
    y = draw_par(30 * mm, y, ptext, size=12, leading=17) - 8

card(30 * mm, 32 * mm, W - 60 * mm, 16 * mm, fill=HexColor("#fff7ed"), stroke=AMBER)
c.setFillColor(HexColor("#9a3412"))
c.setFont("Helvetica-Bold", 11)
c.drawString(35 * mm, 41 * mm, "The gap: there is no unified, offline-first platform that combines patient records, live")
c.drawString(35 * mm, 36 * mm, "monitoring, medical knowledge, and AI risk prediction on local, affordable hardware.")
c.showPage()

# ---------------- Slide 3 — Solution ----------------
header("Solution")
y = draw_par(30 * mm, H - 42 * mm,
             "MediNexus AI is an AI Clinical Copilot that runs entirely on a local machine — no internet, no cloud, "
             "no patient data ever leaving the premises. Five integrated modules, one intelligent orchestrator:",
             size=12, leading=16)

points = [
    ("01", "Unified Patient Records", "Structured SQL records with full CRUD, vitals history, and a live clinical dashboard (bed occupancy, risk counts, disease distribution)."),
    ("02", "Offline Medical Knowledge (RAG)", "FAISS vector search over curated medical references, answered by a local LLM via Ollama + LangChain — cited, grounded answers at the bedside."),
    ("03", "Live Vitals Monitoring", "WebSocket streaming of (simulated) sensor vitals with real-time Plotly charts and threshold alerts."),
    ("04", "AI Risk Prediction", "Lightweight ML models score deterioration risk from vitals trends, flagging high-risk patients before crises."),
    ("05", "Automated Documentation", "One-click discharge summaries and clinical reports generated as PDF/DOCX — reclaiming doctors' time."),
]
box_w = (W - 60 * mm - 4 * 6 * mm) / 5
x = 30 * mm
top = 55 * mm
bh = 68 * mm
for num, title, desc in points:
    card(x, top, box_w, bh)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x + 4 * mm, top + bh - 11 * mm, num)
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 10)
    ty = top + bh - 19 * mm
    for line in wrap_text(title, "Helvetica-Bold", 10, box_w - 8 * mm):
        c.drawString(x + 4 * mm, ty, line)
        ty -= 4.4 * mm
    ty -= 1.5 * mm
    c.setFont("Helvetica", 8.5)
    c.setFillColor(SLATE_600)
    for line in wrap_text(desc, "Helvetica", 8.5, box_w - 8 * mm):
        c.drawString(x + 4 * mm, ty, line)
        ty -= 3.8 * mm
    x += box_w + 6 * mm
c.showPage()

# ---------------- Slide 4 — Dependencies & Showstoppers ----------------
header("Dependencies and Showstoppers")
items = [
    ("1", "Local compute for the LLM",
     "Running an LLM offline needs decent hardware. Mitigation: quantized small models (Phi-3, Gemma 2B) via "
     "Ollama run comfortably on a mid-range laptop — no GPU required."),
    ("2", "Quality of the medical knowledge base",
     "RAG answers are only as good as the corpus. Mitigation: curated, versioned open medical guidelines (WHO, "
     "standard treatment protocols); every answer shows its source citation."),
    ("3", "LLM hallucination in a clinical setting",
     "A wrong AI answer is a patient-safety risk. Mitigation: strict RAG grounding, confidence display, and "
     "human-in-the-loop design — MediNexus assists clinicians, it never auto-diagnoses."),
    ("4", "Real sensor integration",
     "Hackathon build uses a physiologically realistic sensor simulator over WebSockets. Production needs "
     "device vendor APIs/HL7 — the streaming architecture is already designed for that swap."),
]
col_w = (W - 60 * mm - 8 * mm) / 2
row_h = 44 * mm
positions = [(30 * mm, H - 50 * mm - row_h), (30 * mm + col_w + 8 * mm, H - 50 * mm - row_h),
             (30 * mm, H - 56 * mm - 2 * row_h), (30 * mm + col_w + 8 * mm, H - 56 * mm - 2 * row_h)]
for (num, title, desc), (x, yb) in zip(items, positions):
    card(x, yb, col_w, row_h)
    c.setFillColor(ROSE if num in ("2", "3") else TEAL)
    c.circle(x + 8 * mm, yb + row_h - 9 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x + 8 * mm, yb + row_h - 10.5 * mm, num)
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(x + 15 * mm, yb + row_h - 11 * mm, title)
    ty = yb + row_h - 19 * mm
    c.setFont("Helvetica", 9.5)
    c.setFillColor(SLATE_600)
    for line in wrap_text(desc, "Helvetica", 9.5, col_w - 12 * mm):
        c.drawString(x + 6 * mm, ty, line)
        ty -= 4.4 * mm
c.showPage()

# ---------------- Slide 5 — Additional Info ----------------
header("Additional Info — Why It Matters")
y = draw_par(30 * mm, H - 45 * mm,
             "MediNexus AI is offline-first by design: patient data never leaves the hospital premises, which makes "
             "it deployable where privacy rules, budgets, or connectivity make cloud AI impossible. A working "
             "Phase-1 build is already running — live dashboard, patient CRUD, seeded clinical data — and the "
             "remaining modules plug into the same FastAPI + React architecture without refactoring.",
             size=12, leading=17)

stats = [
    ("~65%", "of India's population is rural, served by under 30% of its doctors"),
    ("100%", "offline — zero patient data leaves the premises"),
    ("30 min+", "of documentation time saved per patient via auto-reports"),
    ("< 1 laptop", "total infrastructure needed to deploy the full platform"),
]
box_w = (W - 60 * mm - 3 * 6 * mm) / 4
x = 30 * mm
base = 75 * mm
for big, small in stats:
    card(x, base, box_w, 42 * mm, fill=SLATE)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(x + box_w / 2, base + 27 * mm, big)
    c.setFillColor(SLATE_400)
    c.setFont("Helvetica", 8.5)
    ty = base + 19 * mm
    for line in wrap_text(small, "Helvetica", 8.5, box_w - 8 * mm):
        c.drawCentredString(x + box_w / 2, ty, line)
        ty -= 4 * mm
    x += box_w + 6 * mm

card(30 * mm, 28 * mm, W - 60 * mm, 28 * mm, fill=HexColor("#f0fdfa"), stroke=TEAL)
c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 11)
c.drawString(35 * mm, 48 * mm, "Current status: Phase 1 live and demo-ready")
c.setFont("Helvetica", 10)
c.setFillColor(SLATE_600)
c.drawString(35 * mm, 41 * mm,
             "Working dashboard with 30 seeded patients, full CRUD + search, risk analytics and bed-occupancy "
             "stats — verified end-to-end in the browser.")
c.setFont("Helvetica-Bold", 10)
c.setFillColor(TEAL_DARK)
gh_txt = "GitHub: github.com/MSHREE26092007/medinexus-ai"
c.drawString(35 * mm, 34 * mm, gh_txt)
gh_w = c.stringWidth(gh_txt, "Helvetica-Bold", 10)
c.linkURL("https://github.com/MSHREE26092007/medinexus-ai",
          (35 * mm, 32 * mm, 35 * mm + gh_w, 38 * mm), relative=0)
c.setFont("Helvetica-Bold", 10)
c.setFillColor(TEAL_DARK)
site_txt = "·  Live demo: mshree26092007.github.io/medinexus-ai"
c.drawString(38 * mm + gh_w, 34 * mm, site_txt)
site_w = c.stringWidth(site_txt, "Helvetica-Bold", 10)
c.linkURL("https://mshree26092007.github.io/medinexus-ai/",
          (38 * mm + gh_w, 32 * mm, 38 * mm + gh_w + site_w, 38 * mm), relative=0)
c.setFont("Helvetica", 10)
c.setFillColor(SLATE_600)
c.drawString(41 * mm + gh_w + site_w, 34 * mm, "(full offline version: see README)")
c.showPage()

# ---------------- Slide 6 — Tech Stack ----------------
header("Tech Stack")
stack = [
    ("Frontend", "React + Tailwind CSS + Plotly — responsive clinical dashboard with interactive real-time charts."),
    ("Backend", "FastAPI + WebSockets — REST APIs for records/analytics, live streaming for vitals monitoring."),
    ("Database", "SQLite / PostgreSQL with SQLAlchemy — structured patients, vitals, reports & consultations."),
    ("AI / RAG", "FAISS + Sentence Transformers + LangChain — offline semantic search over medical knowledge."),
    ("Local LLM", "Ollama running Llama 3 / Phi-3 / Gemma — fully offline clinical copilot, zero cloud calls."),
    ("ML & Reports", "PyTorch/TensorFlow risk models + ReportLab & python-docx automated documentation."),
]
col_w = (W - 60 * mm - 2 * 8 * mm) / 3
row_h = 40 * mm
for i, (title, desc) in enumerate(stack):
    x = 30 * mm + (i % 3) * (col_w + 8 * mm)
    yb = (H - 50 * mm - row_h) if i < 3 else (H - 58 * mm - 2 * row_h)
    card(x, yb, col_w, row_h, fill=LIGHT, stroke=HexColor("#e2e8f0"))
    c.setFillColor(TEAL)
    c.rect(x, yb + row_h - 2 * mm, col_w, 2 * mm, fill=1, stroke=0)
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 5 * mm, yb + row_h - 10 * mm, title)
    ty = yb + row_h - 17 * mm
    c.setFont("Helvetica", 9.5)
    c.setFillColor(SLATE_600)
    for line in wrap_text(desc, "Helvetica", 9.5, col_w - 10 * mm):
        c.drawString(x + 5 * mm, ty, line)
        ty -= 4.4 * mm
c.showPage()

# ---------------- Slide 7 — Team ----------------
header("Team — TEAM MEDINEXUS")
members = [
    ("M. Shree", "VIT Chennai", "Chennai", "Member"),
    ("Sanjay K", "VIT Chennai", "Chennai", "Member"),
    ("Niranjan Saravanan", "VIT Chennai", "Chennai", "Member"),
    ("Prajeet Joshua P", "Easwari Engineering College", "Chennai", "Team Leader"),
    ("Sanjeevan U S", "Sri Venkateswara College of Engineering (SVCE)", "Sriperumbudur", "Member"),
]
box_w = (W - 60 * mm - 4 * 5 * mm) / 5
x = 30 * mm
top = 45 * mm
bh = 82 * mm
for name, college, city, role in members:
    card(x, top, box_w, bh, fill=LIGHT, stroke=HexColor("#e2e8f0"))
    c.setFillColor(SLATE if role == "Team Leader" else TEAL)
    c.circle(x + box_w / 2, top + bh - 14 * mm, 8 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x + box_w / 2, top + bh - 16 * mm, name[0])
    ty = top + bh - 29 * mm
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 10.5)
    for line in wrap_text(name, "Helvetica-Bold", 10.5, box_w - 6 * mm):
        c.drawCentredString(x + box_w / 2, ty, line)
        ty -= 4.6 * mm
    ty -= 2 * mm
    c.setFillColor(TEAL_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + box_w / 2, ty, role)
    ty -= 7 * mm
    c.setFillColor(SLATE_600)
    c.setFont("Helvetica", 8.5)
    for line in wrap_text(college, "Helvetica", 8.5, box_w - 6 * mm):
        c.drawCentredString(x + box_w / 2, ty, line)
        ty -= 4 * mm
    c.setFillColor(SLATE_400)
    c.drawCentredString(x + box_w / 2, ty, city)
    x += box_w + 5 * mm

c.setFont("Helvetica", 9)
c.setFillColor(SLATE_400)
c.drawCentredString(W / 2, 30 * mm, "Building healthcare intelligence that works everywhere — even where the internet doesn't.")
c.showPage()

c.save()
print(f"PDF written: {OUT}")
