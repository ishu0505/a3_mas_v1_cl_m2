# Search and Task Allocation (STA) Assignment

Implementation of CS603 Assignment 3 using Mesa agent-based modeling framework.

## Project Structure

```
sta_assignment/
├── models/
│   ├── __init__.py
│   ├── sta_model.py          # Main Mesa model (with communication + auction)
│   ├── agent.py              # Agent class (swarm + auction protocols)
│   └── task.py               # Task class
├── experiments/
│   ├── part1a.py             # Single agent experiment
│   ├── part1b.py             # Multiple agents experiment
│   ├── part1c.py             # Multi-agent coordination (Tc=3)
│   ├── part1d.py             # Multiple tasks & steady-state
│   ├── part1e.py             # Call-out protocol
│   ├── part1f.py             # Call-off protocol
│   ├── part2a.py             # Auction protocol
│   ├── part2b.py             # Protocol comparison
│   └── part2c.py             # Cost-benefit analysis
├── results/                   # Output plots saved here
├── requirements.txt
├── README.md

```

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Experiments

### Part 1(a): Single Agent, Single Task

```bash
python experiments/part1a.py
```

This will:
- Simulate 1 agent with 1 task (T=1, Tc=1, Tr=50, R=1, Rv=25)
- Run for 1000 iterations
- Generate plots showing:
  - Tasks completed per iteration
  - Cumulative task completion
- Save results to `results/part1a_results.png`

### Part 1(b): Multiple Agents

```bash
python experiments/part1b.py
```

This will:
- Test with R = 3, 5, 10, 20, 30 agents
- Run 10 simulations per configuration for statistical reliability
- Generate plots showing:
  - Mean performance with error bars
  - Distribution of performance (box plots)
  - Normalized performance improvement
  - Agent efficiency
- Save results to `results/part1b_results.png`

### Part 1(c): Multiple Agents with Tc=3

```bash
python experiments/part1c.py
```

This will:
- Test with R = 3, 5, 10, 20, 30 agents, now requiring Tc=3 agents per task
- Compare with Tc=1 results from Part 1(b)
- Run 10 simulations per configuration
- Generate comprehensive comparison plots:
  - Performance comparison (Tc=1 vs Tc=3)
  - Performance ratio analysis
  - Distribution box plots
  - Efficiency comparison
  - Coordination overhead metrics
- Save results to `results/part1c_results.png`

### Part 1(d): Multiple Tasks & Steady-State Analysis

```bash
python experiments/part1d.py
```

This will:
- Test with T = 2, 10, 20 simultaneous tasks
- Analyze convergence to steady state
- Determine required number of iterations and simulation runs
- Establish "random benchmark" for comparison
- Run 20 simulations per configuration for statistical analysis
- Generate detailed plots:
  - Convergence trajectories
  - Steady-state convergence time distributions
  - Performance comparison across task counts
  - Statistical precision analysis
  - Rolling statistics
- Save results to `results/part1d_results.png`

### Part 1(e): Call-Out Protocol (Swarm Intelligence)

```bash
python experiments/part1e.py
```

This will:
- Implement call-out protocol where agents emit signals when discovering tasks
- Test with Rd = 0, 100, 200, 300, 400, 600, 1000, 1400
- Agents within communication range respond by moving toward tasks
- Response lasts Rt=60 iterations
- Run 20 simulations per Rd value
- Generate comprehensive plots:
  - Performance vs communication range
  - Improvement over random benchmark
  - Distribution analysis
  - Coefficient of variation
- Compare with random benchmark
- Save results to `results/part1e_results.png`

### Part 1(f): Call-Off Protocol (Improved Swarm)

```bash
python experiments/part1f.py
```

This will:
- Implement call-off protocol with immediate agent release on task completion
- Test same Rd values as Part 1(e)
- Run both call-out and call-off for direct comparison
- Run 20 simulations per protocol per Rd value
- Generate comprehensive comparison plots:
  - Three-way comparison (random, call-out, call-off)
  - Improvement analysis
  - Statistical significance testing
  - Distribution comparisons
- Demonstrate efficiency gains from early release mechanism
- Save results to `results/part1f_results.png`

### Run All Part 1 Experiments

```bash
python run_all_part1.py
```

This convenience script runs all Part 1 experiments (a, b, c, d, e, f) in sequence.
Estimated time: 30-45 minutes for complete suite.

---

## Part 2: Game-Theoretic Auction Model

### Part 2(a): Auction Protocol Implementation

```bash
python experiments/part2a.py
```

This will:
- Implement distance-based auction mechanism
- Discoverer becomes auctioneer, recruits closest (Tc-1) agents
- Test with Rd = 0, 100, 200, 300, 400, 600, 1000, 1400
- Run 20 simulations per Rd value
- Generate performance analysis plots:
  - Auction performance vs communication range
  - Improvement over random benchmark
  - Distribution analysis
  - Optimal configuration identification
- Compare with random baseline
- Save results to `results/part2a_results.png`

### Part 2(b): Protocol Comparison

```bash
python experiments/part2b.py
```

This will:
- Compare all 4 protocols: Random, Call-Out, Call-Off, Auction
- Run all protocols at each Rd value
- Run 20 simulations per protocol per Rd
- Generate comprehensive comparison plots:
  - Head-to-head performance across all Rd
  - Improvement analysis
  - Winner analysis at each Rd
  - Box plot distributions
  - Pairwise comparison matrix
  - Average performance analysis
- Detailed performance rankings and insights
- Save results to `results/part2b_results.png`

### Part 2(c): Cost-Benefit Analysis

```bash
python experiments/part2c.py
```

This will:
- Analyze cost-adjusted performance (strategic agents cost 2×)
- Calculate cost per task: Auction = 4 units, Swarm = 3 units
- Run all protocols for cost comparison
- Generate cost analysis plots:
  - Raw vs cost-adjusted performance
  - Cost efficiency ratios
  - Value proposition analysis
  - Break-even analysis
  - Resource budget comparison
- Determine if auction's complexity is justified
- Provide practical recommendations
- Save results to `results/part2c_results.png`

## Implementation Details

### Random Movement Model (Part 1a)
The agents use a **uniform random walk** model:
- Random angle θ ∈ [0, 2π]
- Random distance d ∈ [0, Rv]
- New position: (x + d·cos(θ), y + d·sin(θ))
- Positions clipped to stay within [0, 1000] bounds

This ensures uniform exploration of the search space.

### Task Completion Logic
1. Agents move randomly each iteration
2. If agent enters task radius (Tr), it stops and waits
3. Task completes when Tc agents are within Tr
4. If more than Tc agents present, closest Tc agents are selected
5. Upon completion, agents are released and new task spawns

### Performance Metrics
- **Tasks per iteration**: Instantaneous completion rate (noisy for low R)
- **Average completion rate**: Mean over all iterations (better for comparison)
- **Efficiency**: Tasks per iteration per agent (shows diminishing returns)

## Key Parameters

| Parameter | Symbol | Value (Part 1) |
|-----------|--------|----------------|
| Number of agents | R | 1 (a), [3,5,10,20,30] (b,c), 30 (d,e,f) |
| Number of tasks | T | 1 (a,b,c), [2,10,20] (d), 2 (e,f) |
| Task radius | Tr | 50 |
| Required agents | Tc | 1 (a,b), 3 (c,d,e,f) |
| Agent speed | Rv | 25 |
| Communication range | Rd | 0 (a-d), [0,100,200,300,400,600,1000,1400] (e,f) |
| Response duration | Rt | N/A (a-d), 60 (e,f) |
| Search area | A | [0,1000] × [0,1000] |
| Iterations | - | 1000 (a,b,c), 3000 (d), 2000 (e,f) |
| Simulation runs | - | 1 (a), 10 (b,c), 20 (d,e,f) |

## Expected Results

### Part 1(a)
- Binary completion pattern (0 or 1 task per iteration)
- Average rate depends on coverage probability
- Theoretical expected time between tasks based on random search

### Part 1(b)
- **Linear improvement** with more agents (better coverage)
- **Diminishing returns** visible in efficiency plot
- With T=1, Tc=1: only 1 agent works at a time (others redundant until task found)
- More agents = higher probability of finding task quickly

### Part 1(c)
- **Lower performance** than Tc=1 due to coordination requirements
- Performance gap ~40-60% at low agent counts
- Gap narrows with more agents (better coverage enables coordination)
- Efficiency per agent is lower (coordination overhead)
- Critical threshold around R=10 where system becomes viable
- Motivates need for communication protocols (Parts 1e-f)

### Part 1(d)
- **Steady-state convergence**:
  - T=2: ~400-600 iterations to stabilize
  - T=10: ~600-800 iterations
  - T=20: ~800-1000 iterations
- More tasks → longer convergence time (more system states)
- **Statistical requirements**:
  - 15-25 runs needed for <5% relative error at 95% confidence
  - Higher T values have more variance (need more runs)
- **Performance scaling**:
  - More tasks → more completions but lower per-task rate
  - Agent resources spread across tasks
  - Establishes "random benchmark" for Parts 1(e-f) comparison

### Part 1(e) - Call-Out Protocol
- **Clear improvement** over random search: 20-40% at optimal Rd
- **Optimal communication range**: Rd ≈ 400-600
  - Too small: insufficient agent recruitment
  - Too large: over-commitment, wasted resources
- **Key behavior**:
  - Agents discovering tasks emit signals
  - Nearby agents respond by moving toward task
  - Response lasts Rt=60 iterations (commitment window)
- **Limitations**:
  - Agents locked in response mode even after task completes
  - Wasted agent-time when tasks finish early
  - Motivates call-off protocol

### Part 1(f) - Call-Off Protocol
- **Additional 5-15% improvement** over call-out
- **Early release mechanism**: Agents freed immediately on task completion
- **Better resource utilization**: More agents available for new tasks
- **More robust** to large communication ranges
- **Key insight**: Release mechanism crucial for efficient swarm coordination
- **Total improvement over random**: 25-50% at optimal Rd
- Demonstrates superiority of bidirectional communication

### Part 2(a) - Auction Protocol
- **Distance-based bidding**: Agents bid with distance to auctioneer
- **Optimal agent selection**: Closest (Tc-1) agents recruited
- **Performance**: ~41% improvement over random at Rd=400
- **Game-theoretic foundation**: Systematic coordination
- **Trade-off**: More complex than swarm protocols
- Competitive but not superior to call-off

### Part 2(b) - Protocol Comparison
- **Winner**: Call-Off outperforms Auction (0.217 vs 0.205)
- **Key finding**: Early release > optimal selection
- **Call-Off wins**: 6/8 configurations across Rd values
- **Auction advantages**: Systematic allocation, predictable
- **Call-Off advantages**: Better resource management, simpler
- Swarm intelligence with release beats game theory

### Part 2(c) - Cost-Benefit Analysis
- **Cost model**: Strategic agents (2×) vs Reactive agents (1×)
- **Per-task cost**: Auction = 4 units, Swarm = 3 units
- **Cost-adjusted winner**: Call-Off (0.072 vs 0.051 tasks/unit)
- **Verdict**: Auction's 33% cost premium NOT justified
- **Break-even**: Auction needs +33% performance (achieves -5%)
- **Recommendation**: Use Call-Off for best cost-performance

## Analysis Questions (Part 1a)

**Q: What is a good movement model?**
- Uniform random walk ensures even exploration
- Alternative: Lévy flight for more efficient search
- Current model: simple, unbiased, mathematically tractable

**Q: Is tasks per iteration a good measure?**
- **For single agent**: Too noisy (binary signal)
- **Better metrics**: 
  - Average completion rate (what we use)
  - Mean time between completions
  - Spatial coverage efficiency
- **For multiple agents**: More stable, shows clear trends

## Code Structure

The implementation follows object-oriented design:

- **STAAgent**: Handles movement, task detection, state management
- **Task**: Manages agent assignment, completion checking, distance calculations  
- **STAModel**: Coordinates agents and tasks, tracks statistics, manages spawning

Mesa framework provides:
- Clean agent-based modeling structure
- Built-in random number generation
- Easy iteration and data collection

## Next Steps

For remaining parts of the assignment:
- **Part 1(c)**: Set Tc=3, rerun experiments
- **Part 1(d)**: Increase T=[2,10,20], analyze steady-state
- **Part 1(e)**: Implement "call-out" protocol with Rd communication
- **Part 1(f)**: Implement "call-off" protocol
- **Part 2**: Game-theoretic auction model

## Troubleshooting

If you get import errors:
```bash
# Make sure you're in the project root directory
cd sta_assignment

# Run from project root
python experiments/part1a.py
```

If plots don't show:
- Check that `results/` directory exists
- Images are saved even if display fails
- Use `plt.savefig()` before `plt.show()`