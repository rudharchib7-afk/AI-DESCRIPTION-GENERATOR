import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Helper for drawing rounded boxes
def draw_box(ax, text, xy, width, height, boxcolor='#eef2f7', edgecolor='#2b5797'):
    box = patches.FancyBboxPatch(xy, width, height, boxstyle='round,pad=0.3',
                                facecolor=boxcolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(box)
    ax.text(xy[0] + width/2., xy[1] + height/2., text,
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827')

def draw_arrow(ax, start, end):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#374151'))

# Figure 2.1: System Architecture
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.5)
ax.axis('off')

draw_box(ax, 'User / Marketer\n(Browser)', (0.5, 2.6), 2.2, 1.0, '#e0f2fe', '#0284c7')
draw_box(ax, 'Frontend UI\n(HTML5/CSS3/JS)', (3.8, 2.6), 2.4, 1.0, '#f0fdf4', '#16a34a')
draw_box(ax, 'PHP Backend Bridge\n(generate.php)', (7.1, 2.6), 2.4, 1.0, '#fef3c7', '#d97706')

draw_box(ax, 'JSON Template DB\n(data.json)', (3.8, 0.4), 2.4, 1.0, '#f3e8ff', '#9333ea')
draw_box(ax, 'Python AI Engine\n(generator.py)', (7.1, 0.4), 2.4, 1.0, '#ffe4e6', '#e11d48')

draw_arrow(ax, (2.7, 3.1), (3.8, 3.1))
draw_arrow(ax, (6.2, 3.1), (7.1, 3.1))
draw_arrow(ax, (8.3, 2.6), (8.3, 1.4))
draw_arrow(ax, (7.1, 0.9), (6.2, 0.9))

plt.tight_layout()
plt.savefig('fig_2_1_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 2.2: Template & Data Flow
fig, ax = plt.subplots(figsize=(8, 2.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')

draw_box(ax, 'Input Payload\n(Name, Tone, Feats, Keywords)', (0.4, 0.8), 2.4, 1.4, '#e0f2fe', '#0284c7')
draw_box(ax, 'Tone & Template Lookup\n(data.json)', (3.7, 0.8), 2.6, 1.4, '#fef3c7', '#d97706')
draw_box(ax, 'Multi-Angle Copy Output\n(Benefit, Story, Feature)', (7.1, 0.8), 2.5, 1.4, '#f0fdf4', '#16a34a')

draw_arrow(ax, (2.8, 1.5), (3.7, 1.5))
draw_arrow(ax, (6.3, 1.5), (7.1, 1.5))

plt.tight_layout()
plt.savefig('fig_2_2_dataflow.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 3.1: Copy Generation Workflow Flowchart
fig, ax = plt.subplots(figsize=(5.5, 6.2))
ax.set_xlim(0, 6)
ax.set_ylim(0, 10)
ax.axis('off')

steps = [
    ('Open Describely Workbench', 9.0),
    ('Input Product Details & Attributes', 7.8),
    ('Validate Inputs & Format Chips', 6.6),
    ('Send POST Request to generate.php', 5.4),
    ('Execute Python generator.py Engine', 4.2),
    ('Load Tone & Match Copy Templates', 3.0),
    ('Trim Word Length & Generate SEO Meta', 1.8),
    ('Display 3 Copy Variations in UI Tabs', 0.6)
]

for idx, (text, y) in enumerate(steps):
    draw_box(ax, text, (1.0, y-0.4), 4.0, 0.7, '#f8fafc', '#475569')
    if idx < len(steps) - 1:
        draw_arrow(ax, (3.0, y-0.4), (3.0, steps[idx+1][1]+0.3))

plt.tight_layout()
plt.savefig('fig_3_1_workflow.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 5.1: Future Expansion Flow
fig, ax = plt.subplots(figsize=(8, 2.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')

draw_box(ax, 'E-Commerce Platform\n(Shopify / WooCommerce)', (0.4, 0.8), 2.5, 1.4, '#f1f5f9', '#475569')
draw_box(ax, 'AI Engine & LLM API\n(OpenAI / Gemini / Custom)', (3.7, 0.8), 2.6, 1.4, '#e0e7ff', '#4338ca')
draw_box(ax, 'Multi-Lingual & Analytics\n(A/B Testing & Export)', (7.1, 0.8), 2.5, 1.4, '#fae8ff', '#c026d3')

draw_arrow(ax, (2.9, 1.5), (3.7, 1.5))
draw_arrow(ax, (6.3, 1.5), (7.1, 1.5))

plt.tight_layout()
plt.savefig('fig_5_1_future_flow.png', dpi=300, bbox_inches='tight')
plt.close()

print('Figures recreated without inner titles!')
