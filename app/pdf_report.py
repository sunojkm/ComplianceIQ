from fpdf import FPDF
from datetime import datetime

def clean(text):
    if not text:
        return ''
    return (str(text)
        .replace('\u2014', '-')
        .replace('\u2013', '-')
        .replace('\u2018', "'")
        .replace('\u2019', "'")
        .replace('\u201c', '"')
        .replace('\u201d', '"')
        .replace('\u2026', '...')
    )

class PDFReport(FPDF):

    def header(self):
        self.set_fill_color(44, 44, 42)
        self.rect(0, 0, 210, 22, 'F')
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(239, 159, 39)
        self.set_xy(10, 5)
        self.cell(0, 12, 'ComplianceIQ', ln=False, align='L')
        self.set_font('Helvetica', '', 9)
        self.set_text_color(180, 178, 169)
        self.set_xy(0, 5)
        self.cell(200, 12, 'ISO 27001 Annex A Security Risk Assessment Report', align='R')
        self.ln(20)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'ComplianceIQ - Confidential | Generated {datetime.now().strftime("%d %b %Y")} | Page {self.page_no()}', align='C')
        
    def amber_heading(self, text):
        self.set_fill_color(44, 44, 42)
        self.set_text_color(239, 159, 39)
        self.set_font('Helvetica', 'B', 11)
        self.set_x(10)
        self.cell(0, 10, f'  {text}', ln=True, fill=True)
        self.ln(2)

    def section_line(self):
        self.set_draw_color(211, 209, 199)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)


def generate_pdf(company_name, industry, business_size, score, risk_level, theme_scores, weaknesses):

    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Cover Info ────────────────────────────────────────────────────────
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(44, 44, 42)
    pdf.set_x(10)
    pdf.cell(0, 12, 'ISO 27001 Annex A', ln=True)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_x(10)
    pdf.cell(0, 10, 'Security Risk Assessment Report', ln=True)
    pdf.ln(4)

    # Company info table
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(95, 94, 90)
    for label, value in [
        ('Organisation', company_name),
        ('Industry',     industry),
        ('Business Size',business_size),
        ('Assessment Date', datetime.now().strftime('%d %B %Y')),
        ('Framework',    'ISO/IEC 27001:2022 Annex A'),
    ]:
        pdf.set_x(10)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(44, 44, 42)
        pdf.cell(45, 7, label + ':', ln=False)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(95, 94, 90)
        pdf.cell(0, 7, value, ln=True)

    pdf.ln(4)
    pdf.section_line()

    # ── Overall Score Banner ──────────────────────────────────────────────
    pdf.ln(4)
    risk_colors = {
        'Low':      (46, 106, 79),
        'Medium':   (239, 159, 39),
        'High':     (230, 81, 0),
        'Critical': (193, 18, 31),
    }
    rc = risk_colors.get(risk_level, (44, 44, 42))

    pdf.set_fill_color(*rc)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_x(10)
    pdf.cell(190, 14, f'  Overall Compliance Score:  {score}%   |   Risk Level:  {risk_level} Risk', ln=True, fill=True)
    pdf.ln(6)

    # ── Theme Scores ──────────────────────────────────────────────────────
    pdf.amber_heading('Theme-Level Compliance Scores')

    for theme, ts in theme_scores.items():
        tc = risk_colors.get(
            'Low' if ts >= 80 else 'Medium' if ts >= 60 else 'High' if ts >= 40 else 'Critical',
            (44, 44, 42)
        )
        pdf.set_x(10)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(44, 44, 42)
        pdf.cell(60, 8, theme, ln=False)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*tc)
        pdf.cell(20, 8, f'{ts}%', ln=False)

        # Progress bar
        bar_x = pdf.get_x() + 4
        bar_y = pdf.get_y() + 2
        pdf.set_fill_color(220, 220, 220)
        pdf.rect(bar_x, bar_y, 80, 4, 'F')
        pdf.set_fill_color(*tc)
        pdf.rect(bar_x, bar_y, 80 * ts / 100, 4, 'F')
        pdf.ln(9)

    pdf.ln(4)
    pdf.section_line()

    # ── Identified Weaknesses ─────────────────────────────────────────────
    pdf.ln(4)
    pdf.amber_heading(f'Identified Weaknesses  ({len(weaknesses)} controls failed)')

    weight_labels = {3: 'Critical', 2: 'Important', 1: 'Advisory'}
    weight_colors = {3: (193, 18, 31), 2: (230, 81, 0), 1: (46, 106, 79)}

    for i, w in enumerate(weaknesses):
        if pdf.get_y() > 260:
            pdf.add_page()

        row_bg = (248, 248, 246) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*row_bg)
        pdf.set_x(10)

        # Control badge
        wc = weight_colors.get(w['weight'], (44, 44, 42))
        pdf.set_fill_color(*wc)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(20, 7, w['control'], fill=True, ln=False, align='C')

        # Theme
        pdf.set_fill_color(*row_bg)
        pdf.set_text_color(95, 94, 90)
        pdf.set_font('Helvetica', '', 8)
        pdf.cell(32, 7, w['theme'], fill=True, ln=False)

        # Weight label
        pdf.set_text_color(*wc)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(22, 7, weight_labels.get(w['weight'], ''), fill=True, ln=False)

        # Question text
        pdf.set_text_color(44, 44, 42)
        pdf.set_font('Helvetica', '', 8)
        pdf.multi_cell(116, 7, clean(w['text']), fill=True)

        if i < len(weaknesses) - 1:
            pdf.set_draw_color(211, 209, 199)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(6)

    # ── Recommended Control Checklist ─────────────────────────────────────
    pdf.add_page()
    pdf.amber_heading(f'Recommended Control Checklist  ({len(weaknesses)} actions)')

    for i, w in enumerate(weaknesses):
        if pdf.get_y() > 260:
            pdf.add_page()

        row_bg = (248, 248, 246) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*row_bg)
        pdf.set_x(10)

        # Control badge — charcoal
        pdf.set_fill_color(44, 44, 42)
        pdf.set_text_color(239, 159, 39)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(20, 7, w['control'], fill=True, ln=False, align='C')

        # Theme
        pdf.set_fill_color(*row_bg)
        pdf.set_text_color(95, 94, 90)
        pdf.set_font('Helvetica', '', 8)
        pdf.cell(32, 7, w['theme'], fill=True, ln=False)

        # Remediation action
        pdf.set_text_color(44, 44, 42)
        pdf.set_font('Helvetica', '', 8)
        pdf.multi_cell(138, 7, clean(w['remediation']), fill=True)

        if i < len(weaknesses) - 1:
            pdf.set_draw_color(211, 209, 199)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    # ── Footer Note ───────────────────────────────────────────────────────
    pdf.ln(8)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.set_x(10)
    pdf.multi_cell(190, 5,
        'This report was generated by ComplianceIQ and is based on self-reported answers to ISO 27001:2022 Annex A control questions. '
        'It does not constitute formal certification or legal compliance advice. '
        'Full Annex A coverage (93 controls) and additional frameworks are available in the post-course roadmap.'
    )

    return bytes(pdf.output())