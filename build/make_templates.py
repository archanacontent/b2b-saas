"""Generates the blank, branded Word templates and the Excel workbook into templates/."""
import os, re
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "templates")
TITLE = "B2B SaaS Product Launch Playbook"
BRAND = "Archana Panda"
URL = "archanacontent.github.io/b2b-saas"
TEAL = "1F4E5A"
TEAL_LIGHT = "DCEBEE"

from build import MODULES  # noqa: E402

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def strip_md(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.replace("**", "").replace("*", "").strip()

def parse_templates(md):
    """Return the template sections (h2 blocks before Worked Example) as (heading, paragraphs, table_rows, bullets)."""
    md = md.split("## Worked Example")[0]
    parts = re.split(r"\n## ", md)
    out = []
    for part in parts[1:]:
        lines = part.strip().split("\n")
        heading = lines[0].strip()
        paras, rows, bullets = [], [], []
        for ln in lines[1:]:
            ln = ln.strip()
            if ln.startswith("|"):
                cells = [c.strip() for c in ln.strip("|").split("|")]
                if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                    continue
                rows.append(cells)
            elif ln.startswith("- "):
                bullets.append(strip_md(ln[2:]))
            elif ln and not ln.startswith("<!--"):
                paras.append(strip_md(ln))
        out.append((heading, paras, rows, bullets))
    return out

def docx_for(i, slug, name, md):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = Cm(2); sec.bottom_margin = Cm(1.8)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    hp = sec.header.paragraphs[0]; hp.text = f"{TITLE}  |  {BRAND}"; hp.runs[0].font.size = Pt(9); hp.runs[0].font.color.rgb = RGBColor.from_string(TEAL)
    fp = sec.footer.paragraphs[0]; fp.text = f"{URL}  |  Licensed under CC BY 4.0"; fp.runs[0].font.size = Pt(8.5); fp.runs[0].font.color.rgb = RGBColor(0x6B, 0x7C, 0x85)
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    t = doc.add_paragraph(); r = t.add_run(f"Module {i} of 9"); r.font.size = Pt(10); r.bold = True; r.font.color.rgb = RGBColor.from_string(TEAL)
    h = doc.add_heading(re.match(r"# (.+)", md).group(1), level=0)
    for run in h.runs: run.font.color.rgb = RGBColor.from_string(TEAL)
    doc.add_paragraph("Blank templates. Fill in the right-hand column, and see the worked example on the playbook site for a completed version.").runs[0].italic = True

    for heading, paras, rows, bullets in parse_templates(md):
        hh = doc.add_heading(heading, level=1)
        for run in hh.runs: run.font.color.rgb = RGBColor.from_string(TEAL)
        for p in paras[:1]:
            doc.add_paragraph(p)
        if rows:
            header, body = rows[0], rows[1:]
            blank_rows = all(all(c == "" for c in r[1:]) for r in body) if body else True
            guidance = (len(header) == 2 and header[1].lower().startswith(("what", "when")))
            if guidance:
                cols = [header[0], "Guidance", "Your entry"]
                data = [[strip_md(r[0]), strip_md(r[1]), ""] for r in body]
            elif blank_rows:
                cols = header
                data = [[strip_md(r[0])] + [""] * (len(header) - 1) for r in body if r[0]] or [[""] * len(header) for _ in range(6)]
                if all(not r[0] for r in data):
                    data = [[""] * len(header) for _ in range(6)]
            else:
                cols = header + ["Your entry"] if len(header) == 2 else header
                data = [[strip_md(c) for c in r] + ([""] if len(header) == 2 else []) for r in body]
            tb = doc.add_table(rows=1, cols=len(cols)); tb.style = "Table Grid"
            for c, txt in zip(tb.rows[0].cells, cols):
                c.text = txt; shade(c, TEAL)
                for run in c.paragraphs[0].runs: run.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            for rdata in data:
                cells = tb.add_row().cells
                for c, txt in zip(cells, rdata):
                    c.text = txt
                if rdata and rdata[0]:
                    shade(cells[0], TEAL_LIGHT)
            for row in tb.rows:
                row.height = Cm(1.0)
            doc.add_paragraph()
        if bullets:
            tb = doc.add_table(rows=1, cols=3); tb.style = "Table Grid"
            for c, txt in zip(tb.rows[0].cells, ["Check", "What it involves", "Done"]):
                c.text = txt; shade(c, TEAL)
                for run in c.paragraphs[0].runs: run.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            for b in bullets:
                k, _, v = b.partition(" - ")
                cells = tb.add_row().cells; cells[0].text = k; cells[1].text = v; cells[2].text = "☐"
                shade(cells[0], TEAL_LIGHT)
            doc.add_paragraph()
    path = os.path.join(OUT, f"{i:02d}-{slug}.docx")
    doc.save(path)
    return path

def workbook():
    wb = Workbook(); wb.remove(wb.active)
    head_fill = PatternFill("solid", fgColor=TEAL); label_fill = PatternFill("solid", fgColor=TEAL_LIGHT)
    thin = Side(style="thin", color="B5CFD4"); box = Border(left=thin, right=thin, top=thin, bottom=thin)

    def sheet(name, title, cols, rows=None, blank=10, widths=None):
        ws = wb.create_sheet(name)
        ws["A1"] = TITLE; ws["A1"].font = Font(bold=True, size=14, color=TEAL)
        ws["A2"] = f"{title}  |  {BRAND}  |  {URL}"; ws["A2"].font = Font(size=10, color="6B7C85")
        for j, c in enumerate(cols, 1):
            cell = ws.cell(row=4, column=j, value=c); cell.font = Font(bold=True, color="FFFFFF"); cell.fill = head_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True); cell.border = box
        data = rows or [[""] * len(cols) for _ in range(blank)]
        for i, r in enumerate(data, 5):
            for j, v in enumerate(r, 1):
                cell = ws.cell(row=i, column=j, value=v); cell.border = box; cell.alignment = Alignment(vertical="top", wrap_text=True)
                if j == 1 and v: cell.fill = label_fill
        for j, w in enumerate(widths or [26] * len(cols), 1):
            ws.column_dimensions[chr(64 + j)].width = w
        ws.freeze_panes = "A5"
        return ws

    ws = sheet("Opportunity Scorecard", "Module 1: Opportunity Scorecard", ["Criterion", "Weight", "Score (1-5)", "Weighted", "Evidence"],
               [["Pain severity", 0.25, None, None, ""], ["Reachable market", 0.20, None, None, ""], ["Willingness to pay", 0.20, None, None, ""],
                ["Competitive gap", 0.15, None, None, ""], ["Fit with current product", 0.10, None, None, ""], ["Time to revenue", 0.10, None, None, ""]],
               widths=[28, 10, 13, 12, 50])
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", showErrorMessage=True, error="Enter a whole number from 1 to 5.")
    ws.add_data_validation(dv)
    for r in range(5, 11):
        ws[f"B{r}"].number_format = "0%"; dv.add(f"C{r}")
        ws[f"D{r}"] = f'=IF(C{r}="","",B{r}*C{r})'; ws[f"D{r}"].number_format = "0.00"
    ws["A12"] = "Weighted total"; ws["A12"].font = Font(bold=True)
    ws["D12"] = "=SUM(D5:D10)"; ws["D12"].number_format = "0.00"; ws["D12"].font = Font(bold=True, size=13, color=TEAL)
    ws["E12"] = '=IF(COUNT(C5:C10)<6,"Score every criterion",IF(D12<3,"Back to research",IF(D12<=3.5,"Move to validation","Ready for positioning")))'
    ws["A13"] = "Score any criterion without evidence as 1."; ws["A13"].font = Font(italic=True, color="6B7C85")

    sheet("Competitor Tracker", "Module 3: Competitor Tracker",
          ["Competitor", "Target buyer", "Core message", "Pricing (date checked)", "Strengths", "Weaknesses", "Recent moves", "Source and date"],
          widths=[22, 24, 28, 24, 26, 26, 24, 26])
    sheet("RACI", "Module 5: RACI Chart", ["Task", "Responsible", "Accountable", "Consulted", "Informed"], widths=[32, 22, 22, 22, 22])
    sheet("Timeline", "Module 5: Launch Timeline", ["Week", "Milestone", "Owner", "Status"],
          [[w, "", "", ""] for w in [-8, -6, -4, -2, 0, 4, 8, 12]], widths=[10, 44, 22, 16])
    sheet("Channel Plan", "Module 5: Channel Plan", ["Channel", "Audience", "Message", "Goal", "Owner"], widths=[18, 28, 40, 22, 20])
    sheet("Campaign Brief", "Module 8: Campaign Brief", ["Field", "Guidance", "Your entry"],
          [["Objective", "The one result the campaign must deliver, as a number.", ""], ["Audience", "ICP segment and persona, with any buying trigger to target.", ""],
           ["Core message", "The headline promise and the pillar this campaign leads with.", ""], ["Offer", "What the buyer gets for responding.", ""],
           ["Channels", "Where the campaign runs, and the job of each channel.", ""], ["Proof", "Evidence cleared for external use.", ""],
           ["Budget and timing", "Spend, start date and length.", ""], ["Success measures", "Leading indicators and the outcome metric, with targets.", ""]],
          widths=[22, 52, 52])
    sheet("KPI Framework", "Module 9: KPI Framework", ["Stage", "Metric", "Target", "Owner", "Data source"],
          [[s, "", "", "", ""] for s in ["Awareness", "Engagement", "Adoption", "Pipeline", "Revenue", "Retention"]], widths=[16, 34, 20, 20, 22])
    ws = sheet("Launch Scorecard", "Module 9: Launch Scorecard", ["Metric", "Target", "Actual", "Status", "Action"], widths=[30, 18, 14, 14, 44])
    sv = DataValidation(type="list", formula1='"Ahead,Close,Behind"', allow_blank=True); ws.add_data_validation(sv); sv.add("D5:D14")
    path = os.path.join(OUT, "launch-playbook-workbook.xlsx"); wb.save(path)
    return path

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, (slug, _, name, _) in enumerate(MODULES, 1):
        print(docx_for(i, slug, name, open(os.path.join(ROOT, "docs", slug + ".md"), encoding="utf-8").read()))
    print(workbook())
