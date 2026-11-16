"""Figures for the 2026-11 underfitted-HMM talk, as plain SVG (no dependencies).

Numbers are copied from ~/Science/Guillaume/underfitted-hmm/results/ (Nov 2026).
Run:  python3 make_figures.py   (writes the .svg files next to this script)
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TEAL = "#0f86a6"     # theory / counted T
BRICK = "#b5532f"    # measurement / Baum-Welch T
REF = "#6f7a80"      # reference lines (gray, always labelled)
INK = "#272d31"
MUTED = "#69737a"
GRID = "#e2e6e8"
FONT = 'font-family="Inter, Century Gothic, sans-serif"'
FS = 1.3  # global text scale, for projection


class Plot:
    """Minimal line/scatter plot on linear or log2 x axis."""

    def __init__(self, w, h, xlim, ylim, xlog=False, margin=(90, 24, 30, 76)):
        self.w, self.h = w, h
        self.l, self.r, self.t, self.b = margin
        self.xlim, self.ylim, self.xlog = xlim, ylim, xlog
        self.out = []

    def X(self, x):
        a, b = self.xlim
        if self.xlog:
            x, a, b = math.log2(x), math.log2(a), math.log2(b)
        return self.l + (x - a) / (b - a) * (self.w - self.l - self.r)

    def Y(self, y):
        a, b = self.ylim
        return self.h - self.b - (y - a) / (b - a) * (self.h - self.t - self.b)

    def text(self, x, y, s, size=17, anchor="start", color=INK, weight=400, extra=""):
        self.out.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size * FS:.0f}" text-anchor="{anchor}" '
            f'fill="{color}" font-weight="{weight}" {FONT} {extra}>{s}</text>')

    def axes(self, xticks, yticks, xlabel, ylabel, xfmt=str, yfmt=str):
        x0, x1 = self.l, self.w - self.r
        y0, y1 = self.h - self.b, self.t
        for v in yticks:
            y = self.Y(v)
            self.out.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
            self.text(x0 - 10, y + 5, yfmt(v), 15, "end", MUTED)
        for v in xticks:
            x = self.X(v)
            self.out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y0}" y2="{y0 + 5}" stroke="{MUTED}" stroke-width="1"/>')
            self.text(x, y0 + 27, xfmt(v), 15, "middle", MUTED)
        self.out.append(f'<line x1="{x0}" x2="{x1}" y1="{y0}" y2="{y0}" stroke="{MUTED}" stroke-width="1"/>')
        self.text((x0 + x1) / 2, self.h - 10, xlabel, 17, "middle", INK)
        cy = (y0 + y1) / 2
        self.text(22, cy, ylabel, 17, "middle", INK, extra=f'transform="rotate(-90 22 {cy:.1f})"')

    def line(self, xs, ys, color, width=2.5, dash=None):
        pts = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in zip(xs, ys))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" '
                        f'stroke-linejoin="round" stroke-linecap="round"{d}/>')

    def dots(self, xs, ys, color, r=5.5):
        for x, y in zip(xs, ys):
            self.out.append(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{color}" '
                            f'stroke="#ffffff" stroke-width="2"/>')

    def hline(self, y, color=MUTED, dash="4 4"):
        self.out.append(f'<line x1="{self.l}" x2="{self.w - self.r}" y1="{self.Y(y):.1f}" y2="{self.Y(y):.1f}" '
                        f'stroke="{color}" stroke-width="1.5" stroke-dasharray="{dash}"/>')

    def save(self, name, title):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}" role="img" aria-label="{title}">'
               f'<title>{title}</title>' + "".join(self.out) + "</svg>\n")
        with open(os.path.join(HERE, name), "w") as f:
            f.write(svg)


# ---------------------------------------------------------------------------
# 1. HMM-RBM fits, held-out gain from the dynamics vs S
#    results/highd_real.md (valid rows): gain with BW T, I(s;s'),
#    and gain + [l(T_cnt,0.01) - l(T_fit)] for the counted T.
S = [2, 4, 8, 16, 32, 64, 128]
gain_bw = [0.050, 0.480, 0.718, 1.009, 0.873, 0.460, -0.183]
d_cnt = [0.0349, 0.0189, 0.0784, 0.1173, 0.4140, 0.9904, 1.7977]
gain_cnt = [g + d for g, d in zip(gain_bw, d_cnt)]
mi_valid = [0.085, 0.492, 0.788, 1.095, 1.355, 1.719, 2.037]

p = Plot(760, 470, (2, 128), (-0.4, 2.2), xlog=True, margin=(96, 200, 24, 76))
p.axes(S, [-0.4, 0, 0.4, 0.8, 1.2, 1.6, 2.0], "number of states S",
       "held-out gain (nats/frame)", yfmt=lambda v: f"{v:g}")
p.hline(0)
p.line(S, mi_valid, REF, 2, dash="6 5")
p.line(S, gain_cnt, TEAL)
p.dots(S, gain_cnt, TEAL)
p.line(S, gain_bw, BRICK)
p.dots(S, gain_bw, BRICK)
p.text(p.X(128) + 12, p.Y(mi_valid[-1]) + 2, "I(ŝ₋₁ ; ŝ₀)", 16, color=INK)
p.text(p.X(128) + 12, p.Y(gain_cnt[-1]) + 14, "counted T", 16, color=INK, weight=600)
p.text(p.X(128) + 12, p.Y(gain_bw[-1]) + 5, "Baum–Welch T", 16, color=INK, weight=600)
p.save("rbm_heldout_gain.svg", "Held-out gain from the dynamics against S, for the Baum-Welch and the counted transition matrix")

# ---------------------------------------------------------------------------
# 2. HMM-RBM fits, training gain vs I(s;s')   (results/highd_real.md, train rows)
gain_tr = [0.068, 0.531, 0.857, 1.149, 1.442, 1.761, 2.084]
mi_tr = [0.094, 0.529, 0.852, 1.158, 1.464, 1.839, 2.214]
p = Plot(470, 470, (0, 2.4), (0, 2.4), margin=(96, 24, 24, 76))
p.axes([0, 0.8, 1.6, 2.4], [0, 0.8, 1.6, 2.4], "I(ŝ₋₁ ; ŝ₀)  (nats)",
       "HMM − mixture (nats/frame)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
p.line([0, 2.4], [0, 2.4], REF, 1.5, dash="6 5")
p.dots(mi_tr, gain_tr, TEAL, r=6.5)
p.text(p.X(2.25), p.Y(2.38), "y = x", 15, "end", MUTED)
for s, x, y in zip(S, mi_tr, gain_tr):
    if s in (4, 16):
        p.text(p.X(x) + 10, p.Y(y) + 22, f"S={s}", 14, color=MUTED)
    if s == 128:
        p.text(p.X(x) - 12, p.Y(y) + 5, f"S={s}", 14, "end", MUTED)
p.save("rbm_gain_vs_mi.svg", "Training gain of the HMM over the mixture against the mutual information of consecutive decoded states")

# ---------------------------------------------------------------------------
# 3. Slow limit, 4-regime truth, K=2, eps=0.01: scan of l(cQ) - l(Q_lumped)
#    results/slow_multiregime.txt
eps, sumN = 0.01, 0.3573
cs = [0.5, 0.7, 1.0, 1.4, 2.0]
meas = [-0.00065, -0.00019, 0.0, -0.00021, -0.00101]
cc = [0.4 + 0.02 * i for i in range(86)]
pred = [eps * (sumN * math.log(c) - (c - 1) * sumN) for c in cc]
p = Plot(560, 420, (0.4, 2.1), (-1.6, 0.2), margin=(100, 175, 24, 76))
p.axes([0.5, 1.0, 1.5, 2.0], [-1.6, -1.2, -0.8, -0.4, 0],
       "scale c of the lumped generator", "ℓ(cQ) − ℓ(Q)  (10⁻³ nats)",
       xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
p.line(cc, [1e3 * v for v in pred], TEAL)
p.dots(cs, [1e3 * v for v in meas], BRICK, r=6.5)
p.text(p.X(2.1) + 10, p.Y(1e3 * pred[-1]) + 5, "expansion", 16, weight=600)
p.text(p.X(2.0) + 12, p.Y(-0.4), "Baum–Welch", 16, weight=600)
p.text(p.X(2.0) + 12, p.Y(-0.4) + 20, "data (dots)", 15, color=MUTED)
p.save("slow_Q_scan.svg", "Loss of likelihood when the lumped generator is scaled by c: measured against the slow expansion")

# ---------------------------------------------------------------------------
# 4. Proportional regime: detectability threshold vs persistence
#    alpha_c * theta^2 = (1 - lambda^2) / (1 + lambda^2)
lam = [i / 100 for i in range(0, 100)]
ac = [(1 - l * l) / (1 + l * l) for l in lam]
p = Plot(560, 420, (0, 1), (0, 1.18), margin=(100, 24, 24, 76))
p.axes([0, 0.25, 0.5, 0.75, 1.0], [0, 0.25, 0.5, 0.75, 1.0],
       "persistence λ of the split", "α_c θ²", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
p.line(lam, ac, TEAL)
p.dots([0], [1], TEAL)
p.text(p.X(0.03), p.Y(1.0) - 14, "i.i.d. labels: BBP", 15, color=MUTED)
p.text(p.X(0.55), p.Y(0.82), "undetectable", 17, "middle", MUTED)
p.text(p.X(0.25), p.Y(0.3), "detectable", 17, "middle", MUTED)
p.save("prop_threshold.svg", "Detectability threshold against the persistence of the hidden labels")

# ---------------------------------------------------------------------------
# 5. Proportional regime: hard phase, alpha_IT / alpha_c vs eta (K*=10, rho=8)
eta = [0, 0.5, 0.8, 0.95]
ratio = [0.94, 0.87, 0.82, 0.79]
p = Plot(470, 420, (0, 1), (0.7, 1.02), margin=(100, 24, 24, 76))
p.axes([0, 0.25, 0.5, 0.75, 1.0], [0.7, 0.8, 0.9, 1.0],
       "persistence η of T*", "α_IT / α_c", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
p.hline(1.0, REF)
p.line(eta, ratio, BRICK)
p.dots(eta, ratio, BRICK, r=6.5)
p.text(p.X(0.02), p.Y(1.0) - 8, "spinodal α_c", 15, color=MUTED)
p.text(p.X(0.5), p.Y(0.755), "hard phase widens", 16, "middle", INK)
p.save("prop_hard_phase.svg", "Ratio of the information-theoretic threshold to the spinodal, K*=10")


# ---------------------------------------------------------------------------
# 6. Schematic: the four limits on a (switching speed, evidence per frame) map
def limits_map():
    W, H = 900, 520
    o = []

    def t(x, y, s, size=18, anchor="middle", color=INK, weight=400):
        o.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    def box(x, y, w, h, color, title, sub):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}" fill-opacity="0.10" '
                 f'stroke="{color}" stroke-width="2"/>')
        t(x + w / 2, y + h / 2 - 6, title, 24, color=INK, weight=600)
        t(x + w / 2, y + h / 2 + 24, sub, 19, color=MUTED)

    L, R, T, B = 110, 870, 30, 450
    o.append(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
             f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
    o.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ar)"/>')
    o.append(f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ar)"/>')
    t((L + R) / 2, B + 40, "persistence of the hidden states", 18)
    t(L + 40, B + 26, "fast", 15, color=MUTED)
    t(R - 40, B + 26, "slow", 15, color=MUTED)
    o.append(f'<text x="44" y="{(T + B) / 2}" font-size="18" text-anchor="middle" fill="{INK}" {FONT} '
             f'transform="rotate(-90 44 {(T + B) / 2})">evidence per frame</text>')
    t(L - 14, B - 12, "weak", 15, "end", MUTED)
    t(L - 14, T + 20, "strong", 15, "end", MUTED)

    box(140, 40, 700, 105, BRICK, "3 · High dimension  d → ∞", "filter one-hot · geometry decides, dynamics = I(ŝ₋₁; ŝ₀)")
    box(140, 175, 330, 120, TEAL, "1 · Fast  T = 1πᵀ + εR", "mixture fit + soft lumping")
    box(510, 175, 330, 120, TEAL, "2 · Slow  T = I + εQ", "hard clustering of regimes")
    box(140, 325, 700, 105, "#6f4aa0", "4 · Proportional  N = αd, Δμ ~ 1/√d", "geometry ~ dynamics ~ noise · thresholds")
    # where the HMM-RBM fits sit
    o.append(f'<circle cx="764" cy="70" r="9" fill="{BRICK}" stroke="#fff" stroke-width="2"/>')
    t(778, 76, "our fits", 16, "start", BRICK, 600)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Map of the four limits"><title>Map of the four limits</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "limits_map.svg"), "w") as f:
    f.write(limits_map())


# ---------------------------------------------------------------------------
# 7. Toy model: a, b close in emission; a <-> c fast; b slow
def toy():
    W, H = 900, 360
    o = []

    def gauss(mu, color, label):
        pts = []
        for i in range(201):
            x = mu - 3 + 6 * i / 200
            y = math.exp(-0.5 * (x - mu) ** 2)
            pts.append(f"{120 + x * 85:.1f},{300 - y * 150:.1f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="2.5"/>')
        o.append(f'<text x="{120 + mu * 85:.1f}" y="140" font-size="28" font-weight="600" text-anchor="middle" '
                 f'fill="{INK}" {FONT}>{label}</text>')

    o.append(f'<line x1="40" y1="300" x2="880" y2="300" stroke="{MUTED}" stroke-width="1.5"/>')
    gauss(1.0, TEAL, "a")
    gauss(2.4, BRICK, "b")
    gauss(7.2, TEAL, "c")
    # delta bracket
    o.append(f'<line x1="{120 + 85:.0f}" y1="325" x2="{120 + 2.4 * 85:.0f}" y2="325" stroke="{INK}" stroke-width="1.5"/>')
    o.append(f'<text x="{120 + 1.7 * 85:.0f}" y="352" font-size="24" text-anchor="middle" fill="{INK}" {FONT}>δ</text>')
    # fast a <-> c arc
    xa, xc = 120 + 85, 120 + 7.2 * 85
    o.append(f'<path d="M{xa},115 C{xa + 120},40 {xc - 120},40 {xc},115" fill="none" stroke="{TEAL}" stroke-width="3" '
             f'marker-end="url(#h)" marker-start="url(#h2)"/>')
    o.append(f'<text x="{(xa + xc) / 2}" y="30" font-size="22" text-anchor="middle" fill="{INK}" {FONT}>fast switching, rate κ</text>')
    # b self loop
    xb = 120 + 2.4 * 85
    o.append(f'<path d="M{xb - 16},118 C{xb - 50},60 {xb + 50},60 {xb + 16},118" fill="none" stroke="{BRICK}" stroke-width="3" marker-end="url(#hb)"/>')
    o.append(f'<text x="{xb - 46}" y="82" font-size="22" text-anchor="end" fill="{INK}" {FONT}>slow</text>')
    defs = (f'<defs>'
            f'<marker id="h" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>'
            f'<marker id="h2" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>'
            f'<marker id="hb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BRICK}"/></marker>'
            f'</defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Toy model: three true states, fit with two"><title>Toy model</title>' + defs + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "toy_model.svg"), "w") as f:
    f.write(toy())

print("figures written to", HERE)
