#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node, shapes
#set page(width: auto, height: auto, margin: 5mm, fill: white)

#let ub(body) = $upright(bold(body))$

#let nodes = (
  ($ub(h)^1$, (0, 1)),
  ($ub(h)^2$, (3, 1)),
  ($ub(h)^3$, (1, 0)),
  ($ub(h)^4$, (2, 2)),
)
#let edges = (
  (3, 2),
  (2, 1),
  (1, 2),
  (0, 3),
  (2, 0),
)

#diagram({
  // Define arbitrary positions for each node (replace with your desired coordinates)

  for (i, (n, pos)) in nodes.enumerate() {
    node(pos, n, stroke: 0.5pt, name: str(i), shape: circle)
  }
  for (from, to) in edges {
    let bend = if (to, from) in edges { 10deg } else { 0deg }
    let lbl = if (from, to) == (2, 1) { $T_(i j)$ } else { none }
    // refer to nodes by label, e.g., <1>
    edge(label(str(from)), label(str(to)), "-|>", bend: bend, label: lbl)
  }
})