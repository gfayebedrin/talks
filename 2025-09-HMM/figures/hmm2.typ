#import "@preview/fletcher:0.5.8": diagram, node, edge

#set page(width: auto, height: auto, margin: 1cm)

#let ub(body) = $upright(bold(body))$

#diagram(
    node-stroke: 0.8pt,
    node-fill: none,
    node-outset: 1pt,
    edge-stroke: 0.8pt,
    node-shape: rect,
    spacing: 6em,

    $
    ub(h)^(s_t) edge(->, T_(s_(t+1) s_t)) edge("d", ->, P(ub(v)_t|ub(h)^(s_t))) &
    ub(h)^(s_(t+1)) edge(->) edge("d", ->) &
    ub(h)^(s_(t+2)) edge("d", ->) \

    ub(v)^(t) &
    ub(v)^(t+1) &
    ub(v)^(t+2) &
    $
)