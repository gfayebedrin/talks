"""Schematic for the reanalysis: why a population vector points to a fixed
angle when all its neurons go quiet together. Plain SVG, no dependencies.
Run: python3 make_pv_artifact.py  (writes pv_artifact.svg next to this file)
Not data: the angles are made up so that their sum points to 36 deg,
as for the selected neurons of the open-loop recording (2025-05-28 run_03).
"""
import math, os

INK, MUTED, ACC, BLUE = "#272d31", "#69737a", "#9b4426", "#2e6da4"
FONT = 'font-family="Inter, Century Gothic, sans-serif"'
W, H, CX, CY, R = 900, 520, 300, 270, 190

raw = [-150, -100, -40, 0, 15, 30, 45, 60, 80, 110, 160, 200]
sx = sum(math.cos(math.radians(a)) for a in raw)
sy = sum(math.sin(math.radians(a)) for a in raw)
rot = 36 - math.degrees(math.atan2(sy, sx))
angles = [a + rot for a in raw]

def pt(a, r):
    t = math.radians(a)
    return CX + r * math.cos(t), CY - r * math.sin(t)

o = [f'<defs>'
     f'<marker id="g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
     f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker>'
     f'<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
     f'</defs>']
o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#d3d9dc" stroke-width="1.5"/>')
for a in angles:
    x, y = pt(a, R * 0.62)
    o.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{MUTED}" stroke-width="2" marker-end="url(#g)"/>')
x, y = pt(36, R * 1.0)
o.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{ACC}" stroke-width="6" marker-end="url(#a)"/>')
x, y = pt(-144, R * 1.0)
o.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{BLUE}" stroke-width="6" stroke-dasharray="12 7" marker-end="url(#b)"/>')

def text(x, y, s, size=24, color=INK, weight=400, anchor="start"):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}" {FONT}>{s}</text>')

lx = 540
text(lx, 70, "grey: preferred direction", 24, MUTED)
text(lx, 100, "of each selected neuron", 24, MUTED)
text(lx, 170, "sum of all preferred", 26, ACC, 600)
text(lx, 202, "directions: 36°", 26, ACC, 600)
text(lx, 300, "all neurons drop together:", 26, BLUE, 600)
text(lx, 332, "the vector moves the", 26, BLUE, 600)
text(lx, 364, "opposite way, to −144°", 26, BLUE, 600)
text(lx, 440, "same direction whatever", 24, MUTED)
text(lx, 470, "the heading was", 24, MUTED)
text(CX, 505, "schematic", 20, MUTED, anchor="middle")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-label="Population vector artifact"><title>Population vector artifact</title>' + "".join(o) + "</svg>\n")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pv_artifact.svg"), "w").write(svg)
