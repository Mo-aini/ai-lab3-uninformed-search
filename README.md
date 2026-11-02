# AI Lab 3 - Uninformed Search

Lab 3 for the AI lab course (CS4944). BFS and DFS traces on the A-G graph from the manual, depth limited search and iterative deepening, and uniform cost search on the weighted version of the graph.

## Files

- `main.py` runs everything
- `src/lab3_bfs_dfs.py` Task 1, BFS and DFS
- `src/lab3_depth_search.py` Task 2, DLS and IDDFS
- `src/lab3_ucs.py` Task 3, UCS vs BFS
- `outputs/output.txt` output of my run
- `report/Lab3_Report_Mohammed_Emad_ALaini.docx` the report with the hand traces

## How to run

Only Python 3 is needed, no extra packages.

```
python main.py
```

## Results

Graph from the manual: A->B, A->C, B->D, B->E, C->F, E->G. Start A, goal G.

| Algorithm | Visit order | Path |
|-----------|-------------|------|
| BFS | A, B, C, D, E, F, G | A-B-E-G |
| DFS | A, B, D, E, G | A-B-E-G |

| DLS limit | Status | Path | Nodes processed |
|-----------|--------|------|-----------------|
| 1 | CUTOFF | - | 3 |
| 2 | CUTOFF | - | 6 |
| 3 | FOUND | A-B-E-G | 5 |
| 4 | FOUND | A-B-E-G | 5 |

IDDFS finds the goal at limit 3 after 15 nodes in total.

For Task 3 I added the corridor C->G with these weights: A->B 1, A->C 2, B->D 4, B->E 1, C->F 3, C->G 10, E->G 1. The manual does not give B->D and C->F, so I chose 4 and 3. They do not change the answer.

| Algorithm | Path | Edges | Cost |
|-----------|------|-------|------|
| BFS | A-C-G | 2 | 12 |
| UCS | A-B-E-G | 3 | 3 |

BFS finds the path with the fewest edges, UCS finds the cheapest one.

## Author

Mohammed Emad ALaini

MIT License, see LICENSE.
