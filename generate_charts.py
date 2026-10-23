import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

output_dir = Path(r"c:\Users\THARUNIKA SS\Downloads\new fly detect 222\paper_figures")
output_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# Chart 1: Academic Benchmark Comparison Across the 5 Hybrid Heads
# -------------------------------------------------------------
models = ['YOLO12 + LSTM\n(Top Best)', 'YOLO12 +\nBiLSTM + Attn', 'YOLO12 + cGAN\n+ Transformer', 'YOLO12 +\nCNN', 'YOLO12 +\nTransformer']
test_acc = [91.98, 88.81, 82.19, 81.05, 78.08]
test_f1 = [92.89, 87.97, 81.77, 79.97, 76.92]
val_acc = [82.43, 76.58, 82.42, 84.07, 81.32]

x = np.arange(len(models))
width = 0.26

plt.figure(figsize=(9, 4.8), dpi=300)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

rects1 = plt.bar(x - width, test_acc, width, label='Test Accuracy (%)', color='#1e40af', edgecolor='black', linewidth=0.6)
rects2 = plt.bar(x, test_f1, width, label='Test Macro F1 (%)', color='#0284c7', edgecolor='black', linewidth=0.6)
rects3 = plt.bar(x + width, val_acc, width, label='Validation Accuracy (%)', color='#94a3b8', edgecolor='black', linewidth=0.6)

plt.ylabel('Score Percentage (%)', fontsize=11, fontweight='bold', labelpad=8)
plt.title('Goodness-of-Fit and Classification Benchmark across 5 Hybrid Heads', fontsize=12, fontweight='bold', pad=12)
plt.xticks(x, models, fontsize=9.5)
plt.ylim(65, 100)
plt.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Value annotations
for rect in rects1:
    h = rect.get_height()
    plt.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    plt.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(output_dir / "figure_benchmarks.png", dpi=300)
plt.close()
print("Saved figure_benchmarks.png")

# -------------------------------------------------------------
# Chart 2: 2x2 Image Collage of Aerial Target Classes
# -------------------------------------------------------------
img_dir = Path(r"c:\Users\THARUNIKA SS\Downloads\new fly detect 222\presentation_images")
plane = Image.open(img_dir / "airplane.jpg").resize((600, 380))
heli = Image.open(img_dir / "helicopter.jpg").resize((600, 380))
drone = Image.open(img_dir / "drone.jpg").resize((600, 380))
kite = Image.open(img_dir / "kite.jpg").resize((600, 380))

fig, axes = plt.subplots(2, 2, figsize=(8.5, 5.6), dpi=300)
axes[0, 0].imshow(plane)
axes[0, 0].set_title("(a) Airplane (Commercial / Jet Transport)", fontsize=10, fontweight='bold', pad=6)
axes[0, 0].axis('off')

axes[0, 1].imshow(heli)
axes[0, 1].set_title("(b) Helicopter (Rotary-Wing Aircraft)", fontsize=10, fontweight='bold', pad=6)
axes[0, 1].axis('off')

axes[1, 0].imshow(drone)
axes[1, 0].set_title("(c) UAV / Drone (Quadcopter Surveillance)", fontsize=10, fontweight='bold', pad=6)
axes[1, 0].axis('off')

axes[1, 1].imshow(kite)
axes[1, 1].set_title("(d) Kite (Aerodynamic Wind-Propelled)", fontsize=10, fontweight='bold', pad=6)
axes[1, 1].axis('off')

plt.subplots_adjust(wspace=0.08, hspace=0.16)
plt.savefig(output_dir / "figure_taxonomy.png", dpi=300, bbox_inches='tight')
plt.close()
print("Saved figure_taxonomy.png")

# -------------------------------------------------------------
# Chart 3: Pipeline Architecture Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
ax.axis('off')

boxes = [
    ("Video Stream\n(MP4 / AVI / MOV)", 0.05, 0.5, 0.15, 0.32, '#e0f2fe', '#0284c7'),
    ("YOLO12 Detector\n(Anchor-Free best.pt)", 0.24, 0.5, 0.16, 0.32, '#dbeafe', '#2563eb'),
    ("ByteTrack Tracker\n(Kalman + Hungarian)", 0.44, 0.5, 0.16, 0.32, '#ede9fe', '#7c3aed'),
    ("MobileNetV3\n(576-dim Tokens)", 0.64, 0.5, 0.15, 0.32, '#fef3c7', '#d97706'),
    ("Hybrid Head\n(LSTM / BiLSTM / cGAN)", 0.83, 0.5, 0.15, 0.32, '#dcfce7', '#16a34a')
]

from matplotlib.patches import FancyBboxPatch

for text, x_c, y_c, w, h, bg_c, border_c in boxes:
    rect = FancyBboxPatch((x_c - w/2, y_c - h/2), w, h, boxstyle="round,pad=0.015,rounding_size=0.02",
                          facecolor=bg_c, edgecolor=border_c, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x_c, y_c, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e293b')

arrows = [(0.125, 0.16), (0.32, 0.36), (0.52, 0.56), (0.715, 0.755)]
for start_x, end_x in arrows:
    ax.annotate('', xy=(end_x, 0.5), xytext=(start_x, 0.5),
                arrowprops=dict(arrowstyle="->", lw=2, color='#475569'))

# Sub-annotation below
ax.text(0.5, 0.18, "Sliding 4-Frame Observation Buffer: Visual Features (576-dim) + Bounding Box Motion Centers (4-dim) = 580-dim Sequence Vector",
        ha='center', va='center', fontsize=9, style='italic', color='#334155',
        bbox=dict(boxstyle="square,pad=0.4", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1))

plt.xlim(0, 1)
plt.ylim(0, 0.8)
plt.tight_layout()
plt.savefig(output_dir / "figure_architecture.png", dpi=300, bbox_inches='tight')
plt.close()
print("Saved figure_architecture.png")
