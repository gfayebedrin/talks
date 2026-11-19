"""Figures for the 2026-11 underfitted-HMM talk, as plain SVG (no dependencies).
Text labels written $...$ are LaTeX, rendered in the deck by plugin/reveal-svg-math.js (img with data-math).

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

    box(140, 40, 700, 105, BRICK, "3 · High dimension", "each frame classified alone, jumps counted")
    box(140, 175, 330, 120, TEAL, "1 · Fast switching", "a mixture plus a little memory")
    box(510, 175, 330, 120, TEAL, "2 · Slow switching", "whole stays sorted by look")
    box(140, 325, 700, 105, "#6f4aa0", "4 · Weak frames", "timing can change the merge")
    # where the HMM-RBM fits sit
    o.append(f'<circle cx="764" cy="70" r="9" fill="{BRICK}" stroke="#fff" stroke-width="2"/>')
    t(778, 76, "our fits", 16, "start", BRICK, 600)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Map of the four limits"><title>Map of the four limits</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "limits_map.svg"), "w") as f:
    f.write(limits_map())


# ---------------------------------------------------------------------------
# 7. Toy model: a, b close in emission; a <-> c fast; b slow
def toy(arrows=True):
    W, H = 900, 350
    base, peak = 340, 150          # baseline y, bump height
    sc, off = 68.85, 167.7          # x in data units -> pixels (x from -2 to 10.2 fits 30..870)
    X = lambda x: off + x * sc
    o = []

    def gauss(mu, color, label):
        pts = [f"{X(mu - 3):.1f},{base}"]
        for i in range(201):
            x = mu - 3 + 6 * i / 200
            pts.append(f"{X(x):.1f},{base - peak * math.exp(-0.5 * (x - mu) ** 2):.1f}")
        pts.append(f"{X(mu + 3):.1f},{base}")
        o.append(f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="2.5"/>')
        o.append(f'<text x="{X(mu):.1f}" y="{base - peak - 12}" font-size="28" font-weight="600" text-anchor="middle" '
                 f'fill="{INK}" {FONT}>{label}</text>')

    o.append(f'<line x1="20" y1="{base}" x2="{W - 20}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>')
    gauss(1.0, TEAL, "a")
    gauss(2.4, BRICK, "b")
    gauss(7.2, "#6f4aa0", "c")
    if arrows:
        # fast a <-> c arc, high enough to clear b's loop
        xa, xc, ye = X(1.0), X(7.2), base - peak - 40
        o.append(f'<path d="M{xa:.1f},{ye} C{xa + 150:.1f},20 {xc - 150:.1f},20 {xc:.1f},{ye}" fill="none" stroke="{TEAL}" '
                 f'stroke-width="3" marker-end="url(#h)" marker-start="url(#h2)"/>')
        o.append(f'<text x="{(xa + xc) / 2:.1f}" y="38" font-size="22" text-anchor="middle" fill="{INK}" {FONT}>fast switching</text>')
        # b self loop, under the arc
        xb = X(2.4)
        o.append(f'<path d="M{xb - 14:.1f},{ye} C{xb - 46:.1f},{ye - 55} {xb + 46:.1f},{ye - 55} {xb + 14:.1f},{ye}" fill="none" '
                 f'stroke="{BRICK}" stroke-width="3" marker-end="url(#hb)"/>')
        o.append(f'<text x="{xb + 34:.1f}" y="{ye - 14}" font-size="22" text-anchor="start" fill="{INK}" {FONT}>slow</text>')
    defs = (f'<defs>'
            f'<marker id="h" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>'
            f'<marker id="h2" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>'
            f'<marker id="hb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{BRICK}"/></marker>'
            f'</defs>')
    y0 = 0 if arrows else 140    # without arrows, drop the empty band on top
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {y0} {W} {H - y0}" width="{W}" height="{H - y0}" role="img" '
            f'aria-label="Toy model: three true states, fit with two"><title>Toy model</title>' + defs + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "toy_model.svg"), "w") as f:
    f.write(toy())
with open(os.path.join(HERE, "toy_model_mixture.svg"), "w") as f:
    f.write(toy(arrows=False))

print("figures written to", HERE)


# ---------------------------------------------------------------------------
# 8. Toy model, the two candidate merges side by side
def two_merges():
    W, H = 1000, 270
    o = []

    def t(x, y, s, size=22, anchor="middle", color=INK, weight=400):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    def panel(x0, groups, title, line1, line2):
        # groups: list of (list of means, color, label)
        sc, base = 50, 250
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x0 + 450}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>')
        for mus, color, label in groups:
            pts = []
            for i in range(301):
                x = -1.5 + 11.6 * i / 300
                y = sum(math.exp(-0.5 * (x - m) ** 2) for m in mus) / len(mus) ** 0.5
                pts.append(f"{x0 + 30 + x * sc * 0.75:.1f},{base - y * 120:.1f}")
            pts = [f"{x0 + 30 - 1.5 * sc * 0.75:.1f},{base}"] + pts + [f"{x0 + 30 + 10.1 * sc * 0.75:.1f},{base}"]
            o.append(f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="2.5"/>')
            for m, letter in zip(mus, label):
                hy = sum(math.exp(-0.5 * (m - mm) ** 2) for mm in mus) / len(mus) ** 0.5
                t(x0 + 30 + m * sc * 0.75, base - hy * 120 - 14, letter, 26, color=color, weight=700)
        t(x0 + 225, 40, title, 26, weight=600)

    panel(30, [([1.0, 2.4], BRICK, "ab"), ([7.2], TEAL, "c")],
          "Merge a and b", "emissions: almost right", "timing: fast and slow mixed")
    panel(530, [([1.0, 7.2], TEAL, "ac"), ([2.4], BRICK, "b")],
          "Merge a and c", "emissions: two far bumps", "timing: clean, a ↔ c is hidden")
    o.append(f'<line x1="500" y1="20" x2="500" y2="260" stroke="{GRID}" stroke-width="2"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="The two candidate merges of the toy model"><title>Two merges</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "two_merges.svg"), "w") as f:
    f.write(two_merges())


# ---------------------------------------------------------------------------
# 9. Deterministic annealing: centres split one at a time as T decreases
def annealing_tree():
    W, H = 760, 460
    o = []

    def t(x, y, s, size=20, anchor="middle", color=INK, weight=400):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    def branch(x_start, x_end, y_start, y_stop, color=TEAL, w=4, y_true=None):
        """Centre position after a split: leaves like sqrt(Tc - T) (sideways).
        Without y_true: reaches x_end at y_stop (quarter-ellipse in (T, x)).
        With y_true: passes x_end (the true mean) at y_true, the true width, and keeps
        drifting outward below it (k-means bias of overlapping clusters)."""
        h = lambda u: math.sqrt(1 - (1 - u) ** 2)
        scale = h((y_true - y_start) / (y_stop - y_start)) if y_true else 1.0
        pts = []
        for k in range(61):
            u = k / 60
            g = h(u) / scale
            pts.append(f"{x_start + (x_end - x_start) * g:.1f},{y_start + (y_stop - y_start) * u:.1f}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{w}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')

    def pos(x_start, x_end, y_start, y_stop, y):
        u = (y - y_start) / (y_stop - y_start)
        return x_start + (x_end - x_start) * math.sqrt(1 - (1 - u) ** 2)

    y0, y1, y2, y3 = 60, 170, 300, 410   # top, first split, second split, true width T*
    y4 = 470                              # bottom of the axis (T -> 0)
    # axis
    o.append(f'<defs><marker id="ta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
             f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
    o.append(f'<line x1="70" y1="{y0}" x2="70" y2="{y4}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ta)"/>')
    o.append(f'<text x="34" y="{(y0 + y4) / 2}" font-size="20" text-anchor="middle" fill="{INK}" {FONT} '
             f'transform="rotate(-90 34 {(y0 + y4) / 2})">temperature T decreases</text>')
    # one centre at the mean, splits into {a,b} and c, then {a,b} splits
    xc, xab, xa, xb, xcc = 400, 300, 220, 380, 600   # mean = (2*300 + 600) / 3
    o.append(f'<line x1="{xc}" y1="{y0}" x2="{xc}" y2="{y1}" stroke="{TEAL}" stroke-width="4"/>')
    branch(xc, xcc, y1, y3)
    # the a+b centre: drawn until it splits, then its two children
    xs = pos(xc, xab, y1, y3, y2)
    pts = [f"{pos(xc, xab, y1, y3, y1 + (y2 - y1) * k / 40):.1f},{y1 + (y2 - y1) * k / 40:.1f}" for k in range(41)]
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/>')
    # a and b overlap: their centres cross the true means at T* and drift apart below it
    branch(xs, xa, y2, y4, y_true=y3)
    branch(xs, xb, y2, y4, y_true=y3)
    # c is well separated: its centre stays on its mean below T*
    o.append(f'<line x1="{xcc}" y1="{y3}" x2="{xcc}" y2="{y4}" stroke="{TEAL}" stroke-width="4"/>')
    o.append(f'<line x1="120" y1="{y3}" x2="720" y2="{y3}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="3 5"/>')
    t(xcc + 14, y3 - 10, "$T^* = 2\\sigma^{*2}$", 30, "start", INK)  # LaTeX: plugin/reveal-svg-math.js
    t(xc + 14, y0 + 8, "one centre at the mean", 18, "start", MUTED)
    t(xa, y4 + 32, "a", 26, weight=600)
    t(xb, y4 + 32, "b", 26, weight=600)
    t(xcc, y4 + 32, "c", 26, weight=600)
    # K = 2 cut
    yk = y2 - 10
    o.append(f'<line x1="120" y1="{yk}" x2="720" y2="{yk}" stroke="{BRICK}" stroke-width="2" stroke-dasharray="8 6"/>')
    t(124, yk - 12, "fit with K = 2 stops here", 19, "start", BRICK, 600)
    t(xc + 14, y1 - 8, "first split", 18, "start", MUTED)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H + 50}" width="{W}" height="{H + 50}" role="img" '
            f'aria-label="Annealing tree"><title>Annealing tree</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "annealing_tree.svg"), "w") as f:
    f.write(annealing_tree())


# ---------------------------------------------------------------------------
# 10. Merging two states breaks the Markov property: a sequence, before and after
def merge_sequence():
    seq = "acacacbbbbbbbbbacacbbbbbbbacac"
    col = {"a": TEAL, "b": BRICK, "c": "#6f4aa0"}
    W, H = 1000, 300
    o = []

    def t(x, y, s, size=20, anchor="middle", color=INK, weight=400):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    x0, w = 140, 28
    t(x0 - 16, 72, "true", 22, "end", weight=600)
    t(x0 - 16, 192, "merged", 22, "end", weight=600)
    for i, s in enumerate(seq):
        o.append(f'<rect x="{x0 + i * w}" y="50" width="{w - 3}" height="34" rx="4" fill="{col[s]}" fill-opacity="0.85"/>')
        t(x0 + i * w + (w - 3) / 2, 74, s, 18, color="#ffffff", weight=600)
        m = "A" if s in "ab" else "C"
        c = BRICK if m == "A" else "#6f4aa0"
        o.append(f'<rect x="{x0 + i * w}" y="170" width="{w - 3}" height="34" rx="4" fill="{c}" fill-opacity="0.45"/>')
        t(x0 + i * w + (w - 3) / 2, 194, m, 18, color=INK, weight=600)
    # brackets for runs of A
    runs, i = [], 0
    while i < len(seq):
        if seq[i] in "ab":
            j = i
            while j < len(seq) and seq[j] in "ab":
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    for i, j in runs:
        xa, xb = x0 + i * w, x0 + j * w - 3
        o.append(f'<path d="M{xa},214 L{xa},222 L{xb},222 L{xb},214" fill="none" stroke="{INK}" stroke-width="1.5"/>')
        t((xa + xb) / 2, 246, str(j - i), 18, color=INK)
    stays = ", ".join(str(j - i) for i, j in runs)
    t(x0, 286, f"steps in A before leaving: {stays}. Short stays from a, long stays from b.", 20, "start", MUTED)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="A merged state mixes short and long stays"><title>Merged sequence</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "merge_sequence.svg"), "w") as f:
    f.write(merge_sequence())


# ---------------------------------------------------------------------------
# 10. Reminder: what an HMM is (hidden chain, observations below)
def hmm_reminder():
    W, H = 900, 330
    o = []

    def t(x, y, s, size=22, anchor="middle", color=INK, weight=400, style=""):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT} {style}>{s}</text>')

    xs = [260 + 150 * i for i in range(5)]
    yh, yo = 90, 250
    t(40, yh + 8, "hidden state", 22, "start", MUTED)
    t(40, yo + 8, "observation", 22, "start", MUTED)
    for i, x in enumerate(xs):
        if i < len(xs) - 1:
            o.append(f'<line x1="{x + 36}" y1="{yh}" x2="{xs[i + 1] - 42}" y2="{yh}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
            t((x + xs[i + 1]) / 2, yh - 16, "T", 22, color=INK, style='font-style="italic"')
        o.append(f'<circle cx="{x}" cy="{yh}" r="34" fill="{TEAL}" fill-opacity="0.15" stroke="{TEAL}" stroke-width="2.5"/>')
        t(x, yh + 9, f"s<tspan font-size='16' dy='6'>{i + 1}</tspan>", 26, color=INK, style='font-style="italic"')
        o.append(f'<line x1="{x}" y1="{yh + 36}" x2="{x}" y2="{yo - 40}" stroke="{MUTED}" stroke-width="2.5" marker-end="url(#am)"/>')
        o.append(f'<rect x="{x - 32}" y="{yo - 32}" width="64" height="64" rx="6" fill="{GRID}" stroke="{MUTED}" stroke-width="2"/>')
        t(x, yo + 9, f"x<tspan font-size='16' dy='6'>{i + 1}</tspan>", 26, color=INK, style='font-style="italic"')
    t(xs[-1] + 70, yh + 8, "…", 28, "start", MUTED)
    t(xs[-1] + 70, yo + 8, "…", 28, "start", MUTED)
    defs = (f'<defs>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="am" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            f'</defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Hidden Markov model: a hidden chain of states, each emitting an observation"><title>HMM</title>'
            + defs + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "hmm_reminder.svg"), "w") as f:
    f.write(hmm_reminder())


# ---------------------------------------------------------------------------
# 11. Toy model, one true hidden sequence (same as the top row of merge_sequence)
def toy_sequence():
    seq = "acacacbbbbbbbbbacacbbbbbbbacac"
    col = {"a": TEAL, "b": BRICK, "c": "#6f4aa0"}
    x0, w = 30, 32
    W, H = x0 * 2 + len(seq) * w, 100
    o = []
    for i, s in enumerate(seq):
        o.append(f'<rect x="{x0 + i * w}" y="10" width="{w - 3}" height="38" rx="4" fill="{col[s]}" fill-opacity="0.85"/>')
        o.append(f'<text x="{x0 + i * w + (w - 3) / 2:.1f}" y="36" font-size="20" text-anchor="middle" fill="#ffffff" '
                 f'font-weight="600" {FONT}>{s}</text>')
    y = 72
    o.append(f'<line x1="{x0}" y1="{y}" x2="{W - x0}" y2="{y}" stroke="{MUTED}" stroke-width="2" marker-end="url(#ta)"/>')
    o.append(f'<text x="{W - x0}" y="{y + 24}" font-size="20" text-anchor="end" fill="{MUTED}" {FONT}>time</text>')
    defs = (f'<defs><marker id="ta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="A sample hidden sequence of the toy model"><title>Toy sequence</title>' + defs + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "toy_sequence.svg"), "w") as f:
    f.write(toy_sequence())


# ---------------------------------------------------------------------------
# 12. Toy model, the hidden sequence after each candidate merge
#     (colours match the groups of two_merges)
def merged_sequences():
    seq = "acacacbbbbbbbbbacacbbbbbbbacac"
    col = {"a": TEAL, "b": BRICK, "c": "#6f4aa0"}
    rows = [("true", lambda s: (s, col[s])),
            ("a+b merged", lambda s: ("ab", BRICK) if s in "ab" else ("c", TEAL)),
            ("a+c merged", lambda s: ("ac", TEAL) if s in "ac" else ("b", BRICK))]
    x0, w, dy = 190, 32, 64
    W, H = x0 + len(seq) * w + 20, 30 + dy * len(rows)
    o = []
    for r, (label, f) in enumerate(rows):
        y = 12 + r * dy
        o.append(f'<text x="{x0 - 18}" y="{y + 26}" font-size="22" text-anchor="end" fill="{INK}" '
                 f'font-weight="600" {FONT}>{label}</text>')
        for i, s in enumerate(seq):
            g, c = f(s)
            o.append(f'<rect x="{x0 + i * w}" y="{y}" width="{w - 3}" height="38" rx="4" fill="{c}" fill-opacity="0.8"/>')
            o.append(f'<text x="{x0 + i * w + (w - 3) / 2:.1f}" y="{y + 25}" font-size="{15 if len(g) > 1 else 19}" '
                     f'text-anchor="middle" fill="#ffffff" font-weight="600" {FONT}>{g}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="The toy hidden sequence after each merge"><title>Merged sequences</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "merged_sequences.svg"), "w") as f:
    f.write(merged_sequences())



# ---------------------------------------------------------------------------
# 14. Dwivedi et al. 2018, case 1 (= our toy): truth 1/4 N(-th(1+r)) + 1/4 N(-th(1-r)) + 1/2 N(th),
#     fit 1/2 N(-t) + 1/2 N(t), sigma = 1 known. theta_bar = 3.005 computed numerically (KL projection).
def em_merge_fit():
    th, rho, tbar = 3.0, 0.4, 3.005
    W, H = 900, 330
    base, sc_y = 290, 1150          # baseline y, px per unit density
    X = lambda x: 450 + x * 58       # x from -7.5 to 7.5
    npdf = lambda x, m: math.exp(-0.5 * (x - m) ** 2) / math.sqrt(2 * math.pi)
    o = []

    def curve(f, color, fill_op, dash=None, w=2.5):
        pts = [f"{X(-7.5):.1f},{base}"] + [f"{X(-7.5 + 15 * i / 300):.1f},{base - sc_y * f(-7.5 + 15 * i / 300):.1f}"
                                         for i in range(301)] + [f"{X(7.5):.1f},{base}"]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="{fill_op}" stroke="{color}" '
                 f'stroke-width="{w}"{d}/>')

    def t(x, y, s, size=26, anchor="middle", color=INK, weight=600):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    o.append(f'<line x1="20" y1="{base}" x2="{W - 20}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>')
    ma, mb = -th * (1 + rho), -th * (1 - rho)
    curve(lambda x: 0.25 * npdf(x, ma), TEAL, 0.15)
    curve(lambda x: 0.25 * npdf(x, mb), BRICK, 0.15)
    curve(lambda x: 0.5 * npdf(x, th), "#6f4aa0", 0.15)
    # fitted two-component model, sigma fixed
    curve(lambda x: 0.5 * npdf(x, -tbar), INK, 0.0, dash="9 6", w=3)
    curve(lambda x: 0.5 * npdf(x, tbar), INK, 0.0, dash="9 6", w=3)
    t(X(ma) - 40, base - sc_y * 0.25 * npdf(0, 0) + 4, "a")
    t(X(mb) + 40, base - sc_y * 0.25 * npdf(0, 0) + 4, "b")
    t(X(th) + 70, base - sc_y * 0.5 * npdf(0, 0) + 30, "c")
    t(X(-tbar), base - sc_y * 0.5 * npdf(0, 0) - 14, "fit", 22, color=INK, weight=600)
    t(X(tbar), base - sc_y * 0.5 * npdf(0, 0) - 14, "fit", 22, color=INK, weight=600)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="A two-component fit to three components: one fitted bump sits on the merged pair">'
            f'<title>EM merge fit</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "em_merge_fit.svg"), "w") as f:
    f.write(em_merge_fit())


# ---------------------------------------------------------------------------
# 15. Toy model fitted with two components (free means, widths, weights), population EM.
#     Truth: a, b, c at 1.0, 2.4, 7.2, sigma = 1, weights 1/3. Fit (computed): merged a+b at 1.708,
#     sd 1.23, weight 0.668; c at 7.209, sd 0.993, weight 0.332.
def toy_fit():
    W, H = 900, 380
    base = 330
    sc, off = 68.85, 167.7
    X = lambda x: off + x * sc
    k = 1128                        # px per unit density
    npdf = lambda x, m, s: math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
    o = []

    def curve(f, color, fill_op, dash=None, w=2.5):
        pts = [f"{X(-2):.1f},{base}"] + [f"{X(-2 + 12.2 * i / 400):.1f},{base - k * f(-2 + 12.2 * i / 400):.1f}"
                                        for i in range(401)] + [f"{X(10.2):.1f},{base}"]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="{fill_op}" stroke="{color}" '
                 f'stroke-width="{w}"{d}/>')

    def t(x, y, s, size=28, color=INK, weight=600):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="middle" fill="{color}" '
                 f'font-weight="{weight}" {FONT}>{s}</text>')

    o.append(f'<line x1="20" y1="{base}" x2="{W - 20}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>')
    for mu, col in ((1.0, TEAL), (2.4, BRICK), (7.2, "#6f4aa0")):
        curve(lambda x, mu=mu: npdf(x, mu, 1) / 3, col, 0.15)
    curve(lambda x: 0.668 * npdf(x, 1.708, 1.23), INK, 0.0, dash="9 6", w=3)
    curve(lambda x: 0.332 * npdf(x, 7.209, 0.993), INK, 0.0, dash="9 6", w=3)
    ytrue = base - k * npdf(0, 0, 1) / 3
    t(X(1.0), base + 34, "a")
    t(X(2.4), base + 34, "b")
    t(X(7.2), base + 34, "c")
    t(X(1.708), base - k * 0.668 * npdf(0, 0, 1.23) - 14, "fit", 24)
    t(X(7.209), ytrue - 14, "fit", 24)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Toy model fitted with two components: one wide component covers a and b">'
            f'<title>Toy fit</title>' + "".join(o) + "</svg>\n")


with open(os.path.join(HERE, "toy_fit.svg"), "w") as f:
    f.write(toy_fit())
