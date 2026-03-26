# Anytime Sequential Halving in Monte-Carlo Tree Search

This repository contains the code accompanying the paper [**Anytime Sequential Halving in Monte-Carlo Tree Search**](https://arxiv.org/abs/2411.07171), published at the *Computers and Games 2024* conference.

**Authors:** Dominic Sagers, Mark H.M. Winands, Dennis J.N.J. Soemers

## Motivation

Monte-Carlo Tree Search (MCTS) typically employs multi-armed bandit (MAB) strategies such as UCB1 to select actions at the root node, optimising for *cumulative* regret. However, at the root of a game tree, what matters is choosing the single best action — making *simple* regret minimisation more appropriate.

Sequential Halving (SH) is a MAB algorithm known to minimise simple regret, but it requires a fixed, predetermined iteration budget. This makes it impractical for use in settings where computation time is variable or unknown in advance (e.g., time-controlled games, automatically generated games, or intelligent time management systems).

This paper introduces **Anytime Sequential Halving**, an adaptive variant of SH that requires no predetermined budget and can be interrupted at any arbitrary point while still returning a satisfactory recommendation. The algorithm repeatedly executes complete passes of SH from scratch — starting with one sample per arm, doubling samples while halving the surviving arms each phase, and restarting from all arms once only one remains.

## Repository Structure

```
Anytime-Sequential-Halving/
├── MAB/                          # Synthetic MAB experiments
│   ├── SequentialHalvingMAB.py   # Implementations: SH, Anytime SH, UCB1
│   ├── MAB_experiment_runner.py  # Experiment runner and plotting utilities
│   ├── MAB_Sequential_Halving_Testing.ipynb  # Full experiment notebook
│   ├── MAB_Sequential_Halving_Testing_Trimmed.ipynb
│   └── Plots/                    # Generated plots from MAB experiments
│
├── Ludii/                        # Board game experiments via the Ludii platform
│   └── AnytimeSequentialHalving/
│       └── src/
│           ├── main/             # Entry point
│           └── mcts/
│               ├── ExampleUCT.java     # Baseline UCT agent
│               ├── SHUCT.java          # SH-UCT agent (standard SH at root)
│               ├── SHUCTAnyTime.java   # Anytime SH-UCT agent (proposed method)
│               ├── SHUCTTime.java      # Time-based SH-UCT variant
│               └── experiment_scripts/ # Scripts to run Ludii game experiments
│
└── Results/                      # Raw and processed results from board game experiments
    ├── process_results.py        # Result parsing and visualisation
    ├── anytimeSH_UCT/            # Anytime SH vs UCT results
    ├── anytimeSH_baseSH/         # Anytime SH vs standard SH results
    ├── base_SH_UCT/              # Standard SH vs UCT results
    └── *.png / *.csv             # Per-game result plots and raw data
```

## Algorithms

### Sequential Halving (SH) — `SequentialHalvingAlg`
The baseline SH algorithm from Karnin et al. (2013). Given a fixed iteration budget `T` and `k` arms, it divides the budget evenly across `⌈log₂(k)⌉` rounds, sampling each surviving arm equally per round and eliminating the worst half after each round.

### Anytime Sequential Halving — `SequentialHalvingAlgAnyTime_v1` / `SHUCTAnyTime.java`
The proposed method. Removes the budget requirement by cycling through full SH passes continuously. Once only one arm remains in a pass, all arms are reintroduced and a new pass begins. This allows the algorithm to be stopped at any time and still output a well-supported recommendation.

### UCB1 / UCT
Provided as a standard baseline for comparison. UCT applies UCB1 within each node of the MCTS tree.

## Games Tested

Board game experiments were conducted via the [Ludii General Game System](https://ludii.games/) across ten games:

| Game | Board Size |
|------|-----------|
| Amazons | 10×10 |
| Atari Go | 9×9 |
| Breakthrough | 8×8 |
| Clobber | 5×6 |
| Gomoku | 15×15 |
| Hex | 11×11 |
| Pentalath | — |
| Reversi | 8×8 |
| Tablut | 9×9 |
| Yavalath | — |

## How to Run

### MAB Experiments

Requirements: Python 3.x, `numpy`, `scipy`, `matplotlib`, `pandas`, `tqdm`

```bash
cd MAB
python MAB_experiment_runner.py
```

Or open and run the notebook interactively:

```bash
jupyter notebook MAB_Sequential_Halving_Testing.ipynb
```

### Board Game Experiments (Ludii)

1. Download the [Ludii platform](https://ludii.games/) and place the `Ludii.jar` in the `lib/` directory.
2. Build the `AnytimeSequentialHalving` Java project (e.g., via Maven or your IDE).
3. Run the experiment scripts in `src/mcts/experiment_scripts/` to pit agents against each other across the ten games.
4. Process raw results with:

```bash
cd Results
python process_results.py
```

## Results

Anytime Sequential Halving is **competitive with standard SH and UCT** across both synthetic MAB problems and board games, despite requiring no predetermined budget. Per-game win-rate plots are available in the `Results/` folder.

## Citation

If you use this code, please cite:

```bibtex
@inproceedings{sagers2024anytime,
  title     = {Anytime Sequential Halving in Monte-Carlo Tree Search},
  author    = {Sagers, Dominic and Winands, Mark H.M. and Soemers, Dennis J.N.J.},
  booktitle = {Computers and Games 2024},
  year      = {2024},
  url       = {https://arxiv.org/abs/2411.07171}
}
```

## References

- Karnin, Z., Koren, T., & Somekh, O. (2013). *Almost Optimal Exploration in Multi-Armed Bandits*. ICML.
- Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002). *Finite-time Analysis of the Multiarmed Bandit Problem*. Machine Learning.
- Cazenave, T. (2015). *Sequential Halving Applied to Trees*. IEEE TCIAIG.
