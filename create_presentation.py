import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE (Aviation Dark Slate Palette matching user's template) ---
    BG_COLOR = RGBColor(31, 46, 60)        # #1F2E3C
    BG_CARD = RGBColor(38, 55, 72)         # #263748
    BG_CARD_LIGHT = RGBColor(46, 66, 86)   # #2E4256
    BORDER_COLOR = RGBColor(58, 83, 108)   # #3A536C
    ACCENT_CYAN = RGBColor(56, 189, 248)   # #38BDF8
    ACCENT_BLUE = RGBColor(96, 165, 250)   # #60A5FA
    ACCENT_GREEN = RGBColor(52, 211, 153)  # #34D399
    ACCENT_GOLD = RGBColor(251, 191, 36)   # #FBBF24
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(165, 185, 205)   # #A5B9CD
    TEXT_DIM = RGBColor(120, 142, 164)     # #788EA4

    FONT_MAIN = "Segoe UI"
    IMG_DIR = Path(r"c:\Users\THARUNIKA SS\Downloads\new fly detect 222\presentation_images")

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="FLYING OBJECT DETECTION SYSTEM"):
        # Category tag with airplane icon
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = f"✈  {category.upper()}"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_CYAN
        p_c.font.name = FONT_MAIN

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.font.name = FONT_MAIN

        # Thin rule divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_COLOR
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title="", items=None, subtitle="", num_badge=None, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = border_color or BORDER_COLOR
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        if num_badge:
            p0.text = f"{num_badge}  {title}"
            p0.font.color.rgb = ACCENT_CYAN
        else:
            p0.text = title
            p0.font.color.rgb = TEXT_WHITE
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.name = FONT_MAIN

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(10)
            p_sub.font.color.rgb = ACCENT_BLUE
            p_sub.font.bold = True
            p_sub.space_before = Pt(3)

        if items:
            for it in items:
                p = tf.add_paragraph()
                p.text = f"• {it}"
                p.font.size = Pt(11)
                p.font.color.rgb = TEXT_MUTED
                p.font.name = FONT_MAIN
                p.space_before = Pt(5)
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Aviation Hero Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s1)

    # Hero Airplane Image on Right Side
    plane_img_path = IMG_DIR / "airplane.jpg"
    if plane_img_path.is_file():
        img = s1.shapes.add_picture(str(plane_img_path), Inches(6.8), Inches(0), Inches(6.533), Inches(7.5))

    # Left Side Content
    # Airplane badge icon
    tag_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5.5), Inches(0.4))
    tf_t = tag_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "✈  COMPUTER VISION & DEEP LEARNING PROJECT"
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = ACCENT_CYAN
    p_t.font.name = FONT_MAIN

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(5.6), Inches(2.2))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_m1 = tf_title.paragraphs[0]
    p_m1.text = "FLYING OBJECT DETECTION"
    p_m1.font.size = Pt(32)
    p_m1.font.bold = True
    p_m1.font.color.rgb = TEXT_WHITE
    p_m1.font.name = FONT_MAIN

    p_m2 = tf_title.add_paragraph()
    p_m2.text = "& CLASSIFICATION"
    p_m2.font.size = Pt(32)
    p_m2.font.bold = True
    p_m2.font.color.rgb = ACCENT_CYAN
    p_m2.font.name = FONT_MAIN

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(5.6), Inches(1.2))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_s = tf_sub.paragraphs[0]
    p_s.text = "A Multi-Stage Aerial Surveillance System Integrating YOLO12 Detection, ByteTrack Trajectory Tracking, and 5 Hybrid Deep Learning Classifier Heads."
    p_s.font.size = Pt(13)
    p_s.font.color.rgb = TEXT_MUTED
    p_s.font.name = FONT_MAIN

    # Project Details Card
    card_info = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(5.4), Inches(1.5))
    card_info.fill.solid()
    card_info.fill.fore_color.rgb = BG_CARD
    card_info.line.color.rgb = BORDER_COLOR
    ci_tb = s1.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(5.0), Inches(1.3))
    ci_tf = ci_tb.text_frame
    ci_p1 = ci_tf.paragraphs[0]
    ci_p1.text = "System Components:"
    ci_p1.font.bold = True
    ci_p1.font.size = Pt(12)
    ci_p1.font.color.rgb = ACCENT_CYAN
    ci_p2 = ci_tf.add_paragraph()
    ci_p2.text = "• Detector: YOLO12 Balanced (Weights: best.pt)\n• Tracker: ByteTrack Multi-Object Temporal Associator\n• Heads: CNN | LSTM | Transformer | BiLSTM+Attn | cGAN"
    ci_p2.font.size = Pt(10.5)
    ci_p2.font.color.rgb = TEXT_MUTED
    ci_p2.space_before = Pt(3)

    # ========================================================
    # SLIDE 2: TABLE OF CONTENTS (Exact replica of user's theme)
    # ========================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s2)

    # Right Side Background Image (Drone / Aerial)
    drone_img = IMG_DIR / "drone.jpg"
    if drone_img.is_file():
        s2.shapes.add_picture(str(drone_img), Inches(7.5), Inches(0), Inches(5.833), Inches(7.5))

    # Left Side: Vertical aircraft accent line
    v_line = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.02), Inches(5.2))
    v_line.fill.solid()
    v_line.fill.fore_color.rgb = ACCENT_CYAN
    v_line.line.fill.background()

    # Airplane icon at top of vertical line
    plane_icon = s2.shapes.add_textbox(Inches(0.85), Inches(0.8), Inches(0.5), Inches(0.4))
    tf_pi = plane_icon.text_frame
    p_pi = tf_pi.paragraphs[0]
    p_pi.text = "✈"
    p_pi.font.size = Pt(18)
    p_pi.font.color.rgb = ACCENT_CYAN

    # Table of Contents Header
    toc_title = s2.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(5.8), Inches(0.6))
    tf_tt = toc_title.text_frame
    p_tt = tf_tt.paragraphs[0]
    p_tt.text = "TABLE OF CONTENTS"
    p_tt.font.size = Pt(26)
    p_tt.font.bold = True
    p_tt.font.color.rgb = TEXT_WHITE
    p_tt.font.name = FONT_MAIN

    # 4 Main Sections (Grid 2x2 matching user's layout)
    sections = [
        ("01", "PROJECT OVERVIEW", "Background, motivation & the 6 flying object classes (drone, airplane, kite, etc.)"),
        ("02", "SYSTEM ARCHITECTURE", "End-to-end video pipeline: YOLO12 detector, ByteTrack & MobileNetV3 feature extractor"),
        ("03", "5 HYBRID CLASSIFIERS", "CNN, LSTM, Transformer, BiLSTM + Attention, and cGAN-augmented Transformer"),
        ("04", "BENCHMARKS & DEPLOYMENT", "Experimental accuracy & F1 test scores, Streamlit Web UI & live output files"),
    ]

    coords = [
        (Inches(1.2), Inches(1.7)),
        (Inches(4.3), Inches(1.7)),
        (Inches(1.2), Inches(4.2)),
        (Inches(4.3), Inches(4.2)),
    ]

    for (num, sec_title, sec_desc), (l, t) in zip(sections, coords):
        box = s2.shapes.add_textbox(l, t, Inches(2.8), Inches(2.1))
        tf_s = box.text_frame
        tf_s.word_wrap = True

        p_num = tf_s.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(36)
        p_num.font.bold = True
        p_num.font.color.rgb = TEXT_WHITE
        p_num.font.name = FONT_MAIN

        p_st = tf_s.add_paragraph()
        p_st.text = sec_title
        p_st.font.size = Pt(13)
        p_st.font.bold = True
        p_st.font.color.rgb = ACCENT_CYAN
        p_st.font.name = FONT_MAIN
        p_st.space_before = Pt(4)

        p_sd = tf_s.add_paragraph()
        p_sd.text = sec_desc
        p_sd.font.size = Pt(10.5)
        p_sd.font.color.rgb = TEXT_MUTED
        p_sd.font.name = FONT_MAIN
        p_sd.space_before = Pt(4)

    # ==========================================
    # SLIDE 3: PROBLEM STATEMENT & CHALLENGES
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s3)
    add_header(s3, "Problem Statement & Aerial Surveillance Challenges", "01. PROJECT OVERVIEW")

    # 3 Cards Layout
    challenges = [
        ("01", "Extreme Scale Variance", "Distant and Miniature Targets", [
            "Flying objects like drones or birds often occupy as few as 15x15 pixels in 1080p footage.",
            "High altitude and distant perspectives cause severe loss of structural visual cues.",
            "Standard detectors trained on general objects suffer high miss rates on small airborne targets."
        ]),
        ("02", "High Velocity & Maneuvering", "Rapid Motion & Frame Exit", [
            "Airborne objects exhibit non-linear acceleration, rapid banking, and high-speed transit.",
            "Motion blur frequently degrades edge contours and texture fidelity.",
            "Single-frame detectors cannot assess velocity or trajectory patterns without temporal context."
        ]),
        ("03", "Inter-Class Visual Ambiguity", "Deceptive Similarities", [
            "From a distance, a soaring bird and an aerodynamic kite exhibit nearly identical static contours.",
            "Commercial airplanes and military drones share planar silhouette traits at sharp angles.",
            "Requires combining spatial appearance with temporal trajectory tracking for robust separation."
        ]),
    ]

    card_w = Inches(3.64)
    card_h = Inches(5.3)
    for idx, (num, title, sub, items) in enumerate(challenges):
        left_pos = Inches(0.8) + idx * Inches(3.9)
        add_card(s3, left_pos, Inches(1.7), card_w, card_h, title, items, subtitle=sub, num_badge=num)

    # ==========================================
    # SLIDE 4: THE 6 TARGET FLYING OBJECT CLASSES
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s4)
    add_header(s4, "Target Aerial Object Classes (Visual Taxonomy)", "01. PROJECT OVERVIEW")

    # 4 Image cards for Airplane, Helicopter, Drone, Kite + notes on Bird & Parachute
    items_to_show = [
        ("AIRPLANE", "High-altitude commercial & passenger airliners, fixed-wing flight patterns", IMG_DIR / "airplane.jpg"),
        ("HELICOPTER", "Rotary-wing aircraft, hover dynamics, rescue & transport flight profiles", IMG_DIR / "helicopter.jpg"),
        ("DRONE (UAV)", "Quadcopter surveillance drones, agile maneuvering, multi-rotor hover", IMG_DIR / "drone.jpg"),
        ("KITE", "High-altitude aerodynamic stunt & leisure kites, wind-propelled dynamics", IMG_DIR / "kite.jpg"),
    ]

    w_box = Inches(2.78)
    h_box = Inches(4.3)
    for i, (name, desc, path) in enumerate(items_to_show):
        x = Inches(0.8) + i * Inches(2.95)
        y = Inches(1.65)

        # Card container
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w_box, h_box)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_COLOR

        # Picture inside card
        if path.is_file():
            s4.shapes.add_picture(str(path), x + Inches(0.12), y + Inches(0.12), w_box - Inches(0.24), Inches(2.2))

        # Text below picture
        tb = s4.shapes.add_textbox(x + Inches(0.12), y + Inches(2.4), w_box - Inches(0.24), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p_n = tf.paragraphs[0]
        p_n.text = name
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = ACCENT_CYAN

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(4)

    # Bottom Banner for Bird and Parachute
    bottom_banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.1), Inches(11.65), Inches(0.95))
    bottom_banner.fill.solid()
    bottom_banner.fill.fore_color.rgb = BG_CARD_LIGHT
    bottom_banner.line.color.rgb = ACCENT_CYAN
    bb_tb = s4.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(11.25), Inches(0.85))
    bb_tf = bb_tb.text_frame
    bb_p = bb_tf.paragraphs[0]
    bb_p.text = "Additional Supported Aerial Classes: BIRD & PARACHUTE"
    bb_p.font.bold = True
    bb_p.font.size = Pt(11)
    bb_p.font.color.rgb = ACCENT_CYAN
    bb_p2 = bb_tf.add_paragraph()
    bb_p2.text = "• Bird: Biological flapping & soaring patterns, distinguished via temporal sequence heads. • Parachute: Canopy descent aerodynamics."
    bb_p2.font.size = Pt(10)
    bb_p2.font.color.rgb = TEXT_WHITE
    bb_p2.space_before = Pt(2)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE & PIPELINE
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s5)
    add_header(s5, "Multi-Stage Aerial Detection & Tracking Architecture", "02. SYSTEM ARCHITECTURE")

    # 5 Horizontal Process Nodes
    steps = [
        ("1. VIDEO INPUT", "Raw Video Stream", [
            "Accepts MP4, AVI, MOV, WebM, MKV.",
            "Decompresses frames sequentially.",
            "Configurable stride (1, 2, 3, 5, 10)."
        ]),
        ("2. YOLO12 DETECTOR", "Object Localization", [
            "Anchor-free YOLO12 balanced weights.",
            "Locates small targets with high recall.",
            "Filters via confidence threshold (0.10)."
        ]),
        ("3. BYTETRACK", "Trajectory Tracking", [
            "Associates bounding boxes over time.",
            "Assigns persistent Tracker IDs.",
            "Extracts 4-frame center motion vectors."
        ]),
        ("4. MOBILENETV3", "Feature Extraction", [
            "Frozen MobileNetV3-Small backbone.",
            "Crops resized & normalized to 224x224.",
            "Produces 576-dim feature tokens."
        ]),
        ("5. HYBRID HEAD", "Classification", [
            "Evaluates spatial/temporal tokens.",
            "Outputs 6-class probability distribution.",
            "Conducts weighted consensus voting."
        ]),
    ]

    node_w = Inches(2.2)
    node_h = Inches(5.3)
    for idx, (title, sub, items) in enumerate(steps):
        left_pos = Inches(0.8) + idx * Inches(2.38)
        add_card(s5, left_pos, Inches(1.7), node_w, node_h, title, items, subtitle=sub, border_color=ACCENT_CYAN if idx in [1, 2, 4] else None)

    # ==========================================
    # SLIDE 6: YOLO12 DETECTION ENGINE
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s6)
    add_header(s6, "Object Detection Engine: YOLO12 Architecture", "02. SYSTEM ARCHITECTURE")

    # Left Column: Key Features
    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3), "YOLO12 Detection Specifications", [
        "State-of-the-Art Architecture: Employs modern area attention and flash attention mechanisms for efficient multi-scale spatial receptive fields.",
        "Balanced Checkpoint: Utilizes the trained YOLO12 balanced weights (best.pt) specifically tuned on multi-class flying objects.",
        "Small Target Sensitivity: Configurable detection threshold down to 0.10 confidence, ensuring distant, sub-30-pixel objects are not missed.",
        "Multi-Resolution Inference: Supports scalable input dimensions (320x320, 416x416, 512x512, 640x640) for balancing GPU/CPU throughput.",
        "Decoupled Classification: Serves as a high-recall region proposal generator, feeding high-fidelity object crops into specialized downstream heads."
    ], subtitle="High-Recall Aerial Localization")

    # Right Column: Helicopter Action Shot + Technical Specs Card
    heli_img = IMG_DIR / "helicopter.jpg"
    if heli_img.is_file():
        s6.shapes.add_picture(str(heli_img), Inches(6.8), Inches(1.7), Inches(5.7), Inches(3.0))

    add_card(s6, Inches(6.8), Inches(4.9), Inches(5.7), Inches(2.1), "Detection Parameters", [
        "Default Confidence: 0.10 (Captures small, distant targets)",
        "Inference Resolution: 640x640 (Optimal edge definition)",
        "Device Support: Seamless auto-switching between CUDA GPU and CPU"
    ], subtitle="Runtime Configuration", border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 7: BYTETRACK SPATIAL & MOTION TRACKING
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s7)
    add_header(s7, "Multi-Object Trajectory Modeling with ByteTrack", "02. SYSTEM ARCHITECTURE")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3), "Why ByteTrack is Vital for Aerial Video", [
        "Low-Score Detection Retention: Unlike standard SORT/DeepSORT which discards detections below 0.5, ByteTrack recovers true low-confidence boxes (e.g. partially occluded or distant objects).",
        "Persistent Track ID Maintenance: Assigns consistent object IDs across consecutive frames, preventing ID switching when objects bank or turn.",
        "Kalman Filter Motion Prediction: Smooths bounding box jitter and predicts target location during temporary occlusions (e.g. flying behind clouds or trees).",
        "Temporal Sequence Construction: Accumulates the last 4 observed bounding box centers [x, y, w, h] to compute directional velocity vectors for the LSTM heads."
    ], subtitle="Continuous Trajectory Association", num_badge="01")

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.3), "Trajectory Feature Representation", [
        "4-Frame Observation Buffer: Maintains a sliding deque of length 4 for every active ByteTrack ID.",
        "Visual + Motion Concatenation: Each observation combines 576 MobileNetV3 visual features with 4 spatial box-center coordinates -> 580-dimensional input vector.",
        "Velocity Modeling: Explicitly encodes direction of travel (dx/dt, dy/dt) and change in scale (dw/dt, dh/dt).",
        "Disambiguation Engine: Crucial for separating flapping birds from soaring kites and steady-altitude UAVs."
    ], subtitle="580-Dimensional Temporal Token", num_badge="02", border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 8: THE 5 HYBRID CLASSIFIER HEADS
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s8)
    add_header(s8, "Deep Dive: The 5 Specialized Classifier Heads", "03. HYBRID CLASSIFIERS")

    heads = [
        ("YOLO12 + CNN", "1D Convolutional Network", [
            "Processes single-frame MobileNet visual tokens.",
            "Two 1D Conv layers (576->128->64) with AdaptiveAvgPool.",
            "Fastest inference head; best for distinct, high-res views."
        ]),
        ("YOLO12 + LSTM", "Temporal Recurrent Head", [
            "Processes 4-frame visual + motion sequences (580-dim).",
            "Hidden dimension: 64; LayerNorm + Linear classifier.",
            "Top benchmark performer: learns acceleration & path dynamics."
        ]),
        ("YOLO12 + Transformer", "Self-Attention Encoder", [
            "2-layer Transformer Encoder with 4 attention heads.",
            "Learns positional spatial token embeddings across crops.",
            "Captures subtle inter-part visual dependencies."
        ]),
        ("YOLO12 + BiLSTM + Attention", "Bidirectional Sequence Head", [
            "Bidirectional LSTM with learned attention pooling.",
            "Processes trajectories forward and backward in time.",
            "Highlights critical transitional frames (e.g. banking turns)."
        ]),
        ("YOLO12 + GAN + Transformer", "Synthetic Augmentation Head", [
            "Trained with conditional GAN (cGAN) synthesized features.",
            "Addresses class imbalance and rare viewing angles.",
            "Improves generalization on out-of-distribution targets."
        ]),
    ]

    card_w = Inches(2.2)
    card_h = Inches(5.3)
    for idx, (title, sub, items) in enumerate(heads):
        left_pos = Inches(0.8) + idx * Inches(2.38)
        add_card(s8, left_pos, Inches(1.7), card_w, card_h, title, items, subtitle=sub, border_color=ACCENT_GREEN if "LSTM" in title else None)

    # ==========================================
    # SLIDE 9: EXPERIMENTAL RESULTS & METRICS
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s9)
    add_header(s9, "Performance Benchmark & Validation Results", "04. BENCHMARKS & DEPLOYMENT")

    # Table on Left Side
    table_shape = s9.shapes.add_table(6, 4, Inches(0.8), Inches(1.7), Inches(6.8), Inches(3.2))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(1.5)
    table.columns[3].width = Inches(1.5)

    headers_text = ["Hybrid Pipeline Head", "Test Accuracy", "Test Macro F1", "Validation Acc"]
    for c_idx, h_text in enumerate(headers_text):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_CARD_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_CYAN

    # Real data from hybrid_test_scores.json & hybrid_validation_scores.json
    scores_data = [
        ("YOLO12 + LSTM (Best)", "91.98%", "92.89%", "82.43%"),
        ("YOLO12 + BiLSTM + Attention", "88.81%", "87.97%", "76.58%"),
        ("YOLO12 + cGAN + Transformer", "82.19%", "81.77%", "82.42%"),
        ("YOLO12 + CNN", "81.05%", "79.97%", "84.07%"),
        ("YOLO12 + Transformer", "78.08%", "76.92%", "81.32%"),
    ]

    for r_idx, row in enumerate(scores_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.name = FONT_MAIN
            if c_idx == 0 and "Best" in val:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            elif c_idx in [1, 2] and r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            else:
                p.font.color.rgb = TEXT_WHITE

    # Key Insights Card on Right
    add_card(s9, Inches(7.9), Inches(1.7), Inches(4.6), Inches(5.3), "Key Empirical Findings", [
        "Temporal Modeling Superiority: The LSTM head achieved the highest overall performance (91.98% Accuracy, 92.89% Macro F1), proving that 4-frame trajectory dynamics are decisive for flying object recognition.",
        "Attention Benefits: BiLSTM with Attention reached 88.81% accuracy, confirming that weighting informative acceleration phases improves classification.",
        "cGAN Synthetic Boost: cGAN augmentation lifted Transformer accuracy from 78.08% to 82.19% (+4.11% gain), showing synthetic feature diversity mitigates aerial class imbalances.",
        "Spatial vs. Motion Tradeoff: CNN heads offer rapid single-frame speed (81.05%), but temporal heads drastically cut false-positive confusions between kites and birds."
    ], subtitle="Empirical Analysis & Takeaways", border_color=ACCENT_GREEN)

    # Bottom Callout Card under table
    add_card(s9, Inches(0.8), Inches(5.1), Inches(6.8), Inches(1.9), "Model Checkpoints Included in Package", [
        "Detector: YOLO12_Hybrid_v2/.../yolo12_balanced/weights/best.pt",
        "Heads: CNN.pt (0.98MB), LSTM.pt (0.68MB), Transformer.pt (1.37MB), BiLSTM_Attention.pt (1.36MB), cGAN_Transformer.pt (1.37MB)",
        "Validation Files: hybrid_validation_scores.json, hybrid_test_scores.json"
    ], subtitle="Production Artifacts", border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 10: VIDEO CONSENSUS & DECISION ENGINE
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s10)
    add_header(s10, "Video-Level Consensus & Decision Aggregation", "04. BENCHMARKS & DEPLOYMENT")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3), "Confidence-Weighted Voting Engine", [
        "Frame-Level Robustness: Flying objects frequently undergo temporary specular reflections, motion blur, or partial occlusion causing single-frame misclassifications.",
        "Weighted Accumulation: Rather than naive unweighted majority voting, each detection contributes its model confidence score to its predicted class bucket.",
        "Mathematical Formulation: Video Score(C) = Sum(Conf_i * I(Class_i == C)) across all detected frames i.",
        "Final Verdict Generation: The class achieving the highest accumulated confidence weight is designated the definitive video-level label with its percentage vote share.",
        "Elimination of Outliers: Transient misdetections (e.g. 1 frame of noise) are easily outvoted by dozens of consistent high-confidence detections."
    ], subtitle="Robust Temporal Aggregation", num_badge="01")

    # Right side: Output Deliverables Card + Kite Visual
    kite_img = IMG_DIR / "kite.jpg"
    if kite_img.is_file():
        s10.shapes.add_picture(str(kite_img), Inches(6.8), Inches(1.7), Inches(5.7), Inches(2.7))

    add_card(s10, Inches(6.8), Inches(4.6), Inches(5.7), Inches(2.4), "Exported Analytics Files", [
        "1. Annotated Video (*_annotated.mp4): Full-framerate video with bounding boxes, tracker IDs, and predicted class labels.",
        "2. Frame Log (*_detections.csv): Timestamped record of every box coordinate, detector confidence, and classifier score.",
        "3. Summary (*_classification.csv): Final video-level predicted class and its total weighted vote share."
    ], subtitle="Comprehensive Output Deliverables", border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 11: STREAMLIT WEB UI & DEPLOYMENT
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s11)
    add_header(s11, "Interactive Deployment: Streamlit Web UI", "04. BENCHMARKS & DEPLOYMENT")

    add_card(s11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3), "Web Interface Capabilities", [
        "Zero-Friction Deployment: Built natively on Streamlit with zero external web server dependencies (active on http://localhost:8501).",
        "Drag & Drop File Upload: Supports MP4, MOV, AVI, MKV, M4V, and WebM video formats directly via browser.",
        "Real-Time Pipeline Switching: Interactive sidebar allows switching between all 5 hybrid heads on the fly without restarting.",
        "Live Inference Preview: Streams processed video frames live with color-coded bounding boxes and tracker identity trails.",
        "Dynamic Hyperparameter Sliders: Real-time control of confidence threshold (0.01 - 0.90), image size (320 - 640), and frame stride (1 - 10).",
        "One-Click Downloads: Direct in-browser download links for processed MP4 videos and analytical CSV reports."
    ], subtitle="Production-Ready Web Application", num_badge="UI")

    # Right Side: Deployment Architecture Card
    add_card(s11, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.3), "Runtime Execution Environment", [
        "Local Server: Running on Uvicorn & Streamlit engine inside Python 3.11 isolated virtual environment (.venv).",
        "Hardware Acceleration: Seamless auto-detection for NVIDIA CUDA GPUs; optimized CPU fallback with PyTorch CPU backend.",
        "One-Click Launcher: Windows batch script (START_WINDOWS.bat / RUN_PROJECT.bat) enables immediate launch with a double-click.",
        "Memory Efficiency: Uses PyTorch's torch.no_grad() and OpenCV streaming decoders to process long video files without RAM overflow.",
        "Output Organization: Automatically organizes runs by timestamp into dedicated video_engine_outputs/ folders."
    ], subtitle="Engine Architecture & Performance", border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s12)
    add_header(s12, "Conclusion & Future Research Directions", "04. BENCHMARKS & DEPLOYMENT")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3), "Project Summary & Accomplishments", [
        "End-to-End Pipeline: Successfully built and verified a complete video analytics pipeline combining YOLO12, ByteTrack, and MobileNetV3.",
        "Temporal Mastery: Demonstrated that modeling 4-frame trajectory sequences with LSTM boosts classification accuracy to 91.98% (outperforming static image models).",
        "cGAN Synthetic Proof: Proved that generative feature augmentation mitigates aerial dataset imbalance, providing a +4.11% accuracy improvement.",
        "Operational Interface: Delivered a fully functional, localized Streamlit application for immediate real-world video processing and analysis."
    ], subtitle="Core Contributions", num_badge="★")

    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.3), "Future Research & Expansion", [
        "1. Thermal & Infrared (IR) Fusion: Integrating dual-spectrum RGB + FLIR thermal cameras for night-time aerial tracking.",
        "2. Edge Hardware Acceleration: Quantizing YOLO12 and LSTM heads into TensorRT / ONNX for deployment on NVIDIA Jetson Orin and drones.",
        "3. Multi-Camera Network Fusion: Correlating ByteTrack IDs across multi-camera radar/optical arrays for airspace monitoring.",
        "4. Joint End-to-End Fine-Tuning: Training detector and sequence classifier jointly with spatio-temporal contrastive loss.",
        "5. Expanded Aerial Classes: Extending taxonomy to gliders, hot air balloons, birds of prey, and hypersonic objects."
    ], subtitle="Roadmap & Next Steps", border_color=ACCENT_CYAN)

    out_path = Path(r"c:\Users\THARUNIKA SS\Downloads\new fly detect 222\Flying_Object_Detection_Presentation.pptx")
    prs.save(str(out_path))
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    build_presentation()

