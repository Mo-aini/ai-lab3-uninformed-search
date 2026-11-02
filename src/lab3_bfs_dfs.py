# Lab 3 - BFS and DFS on the manual graph (Section 3.2)
from collections import deque

# code from the manual (Section 3.2)
graph={"A":["B","C"],"B":["D","E"],"C":["F"],"D":[],"E":["G"],"F":[],"G":[]}

def bfs(start, goal):
    q=deque([(start,[start])]); seen={start}
    while q:
        node,path=q.popleft()
        if node==goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n,path+[n]))

def dfs(start, goal):
    stack=[(start,[start])]; seen=set()
    while stack:
        node,path=stack.pop()
        if node==goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n,path+[n]))


# same BFS/DFS but printing a trace
def _p(path):
    return "-".join(path)


def bfs_trace(start, goal, g=None):
    g = graph if g is None else g
    q = deque([(start, [start])]); seen = {start}
    rows = []
    while q:
        node, path = q.popleft()
        if node == goal:
            rows.append((node, _p(path), "goal test true: stop", [_p(p) for _, p in q]))
            return path, rows
        added = []
        for n in g[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n])); added.append(n)
        rows.append((node, _p(path), ", ".join(added) if added else "none", [_p(p) for _, p in q]))
    return None, rows


def dfs_trace(start, goal, g=None):
    g = graph if g is None else g
    stack = [(start, [start])]; seen = set()
    rows = []
    while stack:
        node, path = stack.pop()
        if node == goal:
            rows.append((node, _p(path), "goal test true: stop", [_p(p) for _, p in stack]))
            return path, rows
        if node in seen:
            rows.append((node + " (skipped duplicate)", _p(path), "none", [_p(p) for _, p in stack]))
            continue
        seen.add(node)
        pushed = []
        for n in reversed(g[node]):
            stack.append((n, path + [n])); pushed.append(n)
        rows.append((node, _p(path), ("push " + ", ".join(pushed)) if pushed else "none", [_p(p) for _, p in stack]))
    return None, rows


def print_trace(title, rows, frontier_label):
    print(title)
    print("step | processed node | path to node | successors added | %s" % frontier_label)
    print("0 | - | - | - | [A]")
    for i, (node, path, added, frontier) in enumerate(rows, 1):
        print(i, node, path, added, "[" + ", ".join(frontier) + "]", sep=" | ")


def main():
    print("=" * 72)
    print("LAB 3 / Task 1  BFS and DFS on the supplied A-G graph (start A, goal G)")
    print("=" * 72)
    print("graph =", graph)
    print()
    bpath, brows = bfs_trace("A", "G")
    print_trace("BFS trace (FIFO queue, successors left to right):", brows, "queue after step (front -> back)")
    print("BFS visit order:", ", ".join(r[0] for r in brows))
    print("BFS final path :", " -> ".join(bpath))
    print()
    dpath, drows = dfs_trace("A", "G")
    print_trace("DFS trace (LIFO stack, successors pushed in reversed order):", drows, "stack after step (bottom -> top)")
    print("DFS visit order:", ", ".join(r[0] for r in drows))
    print("DFS final path :", " -> ".join(dpath))
    print()
    print("Verification against the supplied code:")
    print("  print(bfs('A','G')) ->", bfs("A", "G"), "| trace agrees:", bfs("A", "G") == bpath)
    print("  print(dfs('A','G')) ->", dfs("A", "G"), "| trace agrees:", dfs("A", "G") == dpath)


if __name__ == "__main__":
    main()
