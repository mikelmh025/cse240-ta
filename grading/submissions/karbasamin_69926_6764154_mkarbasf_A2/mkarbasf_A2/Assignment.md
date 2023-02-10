---
author: 'Amin Karbas <mkarbasf@ucsc.edu>'
title: 'CSE240 - Assignment 2'
date: '02/06/2023'
geometry: margin=1in
...

# 1. What heuristic was used and why?

I came up with a set of rules that give the most pririty to paths leading to four pieces next to each other, then three if both sides of the three are empty, then three if one side is empty, then two, and so on. This can be found at the top of the `Player.py` file:

```python
evals = {
    1: [
        ('1111', 1000), ('01110', 100),
        ('0111', 70), ('1110', 70),
        ('01100', 20), ('00110', 20),
        ('0011', 10), ('0110', 10), ('1100', 10),
    ],
}
evals[2] = [(run[0].replace('1', '2'), run[1]) for run in evals[1]]
```

This heuristic is intended to be a naive version of a convolutional filter, where specific patterns are recognized and valued; thus highlighting the scenarios that can lead to a win or a loss quickly.

# 2. How does the algorithm perform in time ocntraints?

On my computer (Apple MacBook Pro; M1 Pro), the following times are observed for different depths.

| Depth | AlaphaBeta Time (s) | ExpectiMax Time (s) |
| ----- | ------------------- | ------------------- |
|    2  |    0.01             |     0.01            |
|    3  |    0.06             |     0.07            |
|    4  |    0.53             |     0.51            |
|    5  |    1.05             |     3.55            |
|    6  |   21.28             |    25.07            |
|    7  |   55.53             |   175.79            |


Note that the numbers are on par with the branching factor of at most 7. Also note that AlphaBeta is faster than ExpectiMax, as the pruning limits the costs.

# 3. Can you beat it?

Almost always; which tells me it's still too weak.

# 4. When the algorithm plays itself, does the first player do better or worse in general?

The first player consistently wins. The algorithm is very deterministic, and the evaluation function fairly simple. I estimate that a more involved evaluation function or "a dash of stochastisism" would significantly change this.

