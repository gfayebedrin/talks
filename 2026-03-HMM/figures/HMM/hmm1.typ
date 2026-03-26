#import "@preview/fletcher:0.5.8": diagram, node, edge

#set page(width: auto, height: auto, margin: 1cm)

#let ub(body) = $upright(body)$

#diagram(
    node-stroke: 0.8pt,
    node-fill: none,
    node-outset: 1pt,
    edge-stroke: 0.8pt,
    node-shape: rect,
    spacing: 6em,

    $
    s_t edge(->, P(s_(t+1)|s_t)) edge("d", ->, P(o_t|s_t)) &
    s_(t+1) edge(->) edge("d", ->) &
    s_(t+2) edge("d", ->) \

    o_t &
    o_(t+1) &
    o_(t+2) &
    $
)