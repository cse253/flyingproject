import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (Matching the user's uploaded aviation template) ---
BG_COLOR = RGBColor(33, 49, 64)       # Deep slate navy (#213140)
BG_LIGHT = RGBColor(41, 60, 78)       # Slightly lighter navy for cards (#293C4E)
CARD_BG = RGBColor(38, 55, 72)        # Card fill (#263748)
CARD_BORDER = RGBColor(60, 85, 110)   # Card border (#3C556E)
ACCENT_BLUE = RGBColor(56, 189, 248)  # Cyan / Sky blue (#38BDF8)
ACCENT_GOLD = RGBColor(251, 191, 36)  # Amber gold accent (#FBBF24)
TEXT_WHITE = RGBColor(255, 255, 255)  # Crisp white
TEXT_MUTED = RGBColor(160, 178, 198)  # Soft silver/ice blue (#A0B2C6)
TEXT_DIM = RGBColor(120, 140, 160)    # Subdued gray-blue (#788CA0)
BORDER_COLOR = RGBColor(55, 78, 102)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text="FLYING OBJECT DETECTION SYSTEM"):
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = f"✈  {category_text.upper()}"
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_BLUE
    p_c.font.name = FONT_HEADING

    # Main slide title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.font.name = FONT_HEADING

    # Subtle horizontal line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_COLOR
    line.line.color.rgb = BORDER_COLOR

def add_card(slide, left, top, width, height, title, content_list=None, badge=None, border_color=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color or CARD_BORDER
    card.line.width = Pt(1)

    tx_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    if badge:
        p0.text = f"{badge}  {title}"
    else:
        p0.text = title
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_WHITE
    p0.font.name = FONT_HEADING

    if content_list:
        for item in content_list:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MUTED
            p.font.name = FONT_BODY
            p.space_before = Pt(6)

    return card

