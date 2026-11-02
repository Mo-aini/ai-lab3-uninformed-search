# Lab 3 Task 3 - weighted graph, UCS vs BFS
# I added the corridor C -> G. The manual gives A-C-G = 12 and A-B-E-G = 3.
# B->D and C->F are not given in the manual so I picked 4 and 3.
#   A->B 1  A->C 2  B->D 4  B->E 1  C->F 3  C->G 10  E->G 1
# ties in the queue are broken by insertion order (the counter)
import heapq
from collections import deque

WEIGHTED = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 4), ("E", 1)],
    "C": [("F", 3), ("G", 10)],      # C -> G is the corridor I added
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}


def ucs(graph, start, goal):
    counter = 0
    pq = [(0, counter, start, [start])]
    best = {start: 0}
    order, log = [], []
    while pq:
        cost, _, node, path = heapq.heappop(pq)
        if cost != best.get(node):                     # stale entry: a cheaper path was found later
            log.append((node, cost, "-".join(path), "stale entry ignored", ""))
            continue
        order.append(node)
        if node == goal:
            log.append((node, cost, "-".join(path), "goal processed: stop", frontier_str(pq)))
            return cost, path, order, log
        pushed = []
        for nxt, w in graph.get(node, []):
            ng = cost + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                counter += 1
                heapq.heappush(pq, (ng, counter, nxt, path + [nxt]))
                pushed.append("%s(g=%d+%d=%d)" % (nxt, cost, w, ng))
        log.append((node, cost, "-".join(path), ", ".join(pushed) if pushed else "none", frontier_str(pq)))
    return None, None, order, log


def frontier_str(pq):
    return "[" + ", ".join("%s:%d" % ("-".join(p), c) for c, _, n, p in sorted(pq)) + "]"


def bfs_weighted_topology(graph, start, goal):
    q = deque([(start, [start])]); seen = {start}; order = []
    while q:
        node, path = q.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for n, _w in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
    return None, order


def path_cost(graph, path):
    total, parts = 0, []
    for u, v in zip(path, path[1:]):
        w = dict(graph[u])[v]
        parts.append("%s->%s=%d" % (u, v, w))
        total += w
    return total, " + ".join(parts)


def main():
    print("=" * 72)
    print("LAB 3 / Task 3  Weighted corridor extension: UCS vs BFS")
    print("=" * 72)
    print("Edge weights (directed, successor order as listed):")
    for u, edges in WEIGHTED.items():
        for v, w in edges:
            print("  %s -> %s : %d%s" % (u, v, w, "   (added corridor, Section 3.7)" if (u, v) == ("C", "G") else ""))
    print()
    cost, path, order, log = ucs(WEIGHTED, "A", "G")
    print("UCS processing log:")
    print("step | node | g | path | pushed / note | frontier after (path:g, cheapest first)")
    for i, row in enumerate(log, 1):
        print(i, *row, sep=" | ")
    print("UCS processing order:", ", ".join(order))
    total, expr = path_cost(WEIGHTED, path)
    print("UCS path:", "-".join(path), "| reported cost", cost, "| independent sum", expr, "=", total,
          "| agree:", total == cost)
    print()
    bpath, border = bfs_weighted_topology(WEIGHTED, "A", "G")
    btotal, bexpr = path_cost(WEIGHTED, bpath)
    print("BFS processing order:", ", ".join(border))
    print("BFS path:", "-".join(bpath), "| hops", len(bpath) - 1, "| cost", bexpr, "=", btotal)
    print()
    print("algorithm | path | hops | total cost")
    print("BFS", "-".join(bpath), len(bpath) - 1, btotal, sep=" | ")
    print("UCS", "-".join(path), len(path) - 1, total, sep=" | ")
    print()
    print("Edge-case tests:")
    print("  start == goal (A->A):", ucs(WEIGHTED, "A", "A")[:2])
    print("  unreachable goal (D->G):", ucs(WEIGHTED, "D", "G")[:2], "(None = no path)")
    cyc = {k: list(v) for k, v in WEIGHTED.items()}; cyc["E"] = [("B", 1), ("G", 1)]
    c, p, o, _ = ucs(cyc, "A", "G")
    print("  cyclic graph (added E->B, weight 1):", c, "-".join(p), "processing order", ", ".join(o))


if __name__ == "__main__":
    main()
