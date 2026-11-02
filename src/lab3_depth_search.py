# Lab 3 Task 2 - depth limited search and iterative deepening
# depth = number of edges (A is depth 0). I only check for cycles on the current path.
# FOUND = goal found, CUTOFF = the limit stopped it, FAILURE = nothing left to search
try:
    from .lab3_bfs_dfs import graph as GRAPH
except ImportError:                     # so it also runs as: python src/lab3_depth_search.py
    from lab3_bfs_dfs import graph as GRAPH

FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"


def dls(graph, start, goal, limit):
    processed = []

    def recurse(node, path, depth):
        processed.append(node)
        if node == goal:
            return FOUND, path
        children = [n for n in graph.get(node, []) if n not in path]   # skip nodes already on this path
        if depth == limit:
            # hit the limit: only CUTOFF if there was something deeper
            return (CUTOFF, None) if children else (FAILURE, None)
        cutoff = False
        for n in children:
            status, result = recurse(n, path + [n], depth + 1)
            if status == FOUND:
                return FOUND, result
            if status == CUTOFF:
                cutoff = True
        return (CUTOFF, None) if cutoff else (FAILURE, None)

    status, path = recurse(start, [start], 0)
    return status, path, processed


def iddfs(graph, start, goal, max_depth):
    attempts = []
    for limit in range(0, max_depth + 1):
        status, path, processed = dls(graph, start, goal, limit)
        attempts.append((limit, status, processed))
        if status == FOUND:
            return FOUND, path, attempts
        if status == FAILURE:            # searched everything, a bigger limit will not help
            return FAILURE, None, attempts
    return CUTOFF, None, attempts


def show_path(p):
    return "-".join(p) if p else "-"


def main(graph=GRAPH):
    print("=" * 72)
    print("LAB 3 / Task 2  DLS and IDDFS (root depth 0, path-local cycle check)")
    print("=" * 72)
    print("DLS on the original graph, start A, goal G:")
    print("limit | status | path | nodes processed | processing order")
    for limit in (1, 2, 3, 4):
        status, path, processed = dls(graph, "A", "G", limit)
        print(limit, status, show_path(path), len(processed), ", ".join(processed), sep=" | ")
    print()
    print("IDDFS with maximum depth 1, 2, 3 and 4:")
    print("max depth | status | path | limits attempted (status, nodes) | total nodes processed")
    for md in (1, 2, 3, 4):
        status, path, attempts = iddfs(graph, "A", "G", md)
        tried = "; ".join("L%d %s %d" % (l, s, len(p)) for l, s, p in attempts)
        total = sum(len(p) for _, _, p in attempts)
        print(md, status, show_path(path), tried, total, sep=" | ")
    print()
    print("Per-iteration processing order for IDDFS(max depth 4) - shows the repeated shallow work:")
    _, _, attempts = iddfs(graph, "A", "G", 4)
    for l, s, p in attempts:
        print("  limit %d: %s -> %s" % (l, ", ".join(p), s))
    print()
    print("Edge-case tests (Section 3.8):")
    s, p, pr = dls(graph, "G", "G", 0)
    print("  start == goal (G->G, limit 0):", s, show_path(p), "processed", pr)
    s, p, pr = dls(graph, "C", "G", 4)
    print("  unreachable goal (C->G, limit 4):", s, show_path(p), "processed", pr)
    cyclic = dict(graph); cyclic["E"] = ["B", "G"]; cyclic["D"] = ["A"]
    print("  cyclic graph (added E->B and D->A):", cyclic)
    for limit in (2, 3, 6):
        s, p, pr = dls(cyclic, "A", "G", limit)
        print("    DLS limit %d: %s %s, processed %d nodes (no infinite loop)" % (limit, s, show_path(p), len(pr)))
    s, p, pr = dls(cyclic, "A", "Z", 10)
    print("    cyclic graph, goal Z not in graph, limit 10:", s, "- path-local check prunes cycles, so the search ends")


if __name__ == "__main__":
    main()
