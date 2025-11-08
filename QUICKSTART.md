# CS603 Assignment 3 - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd sta_assignment
pip install -r requirements.txt
```

### 2. Run a Single Experiment

```bash
# Quick test - Part 1(a) - runs in ~30 seconds
python experiments/part1a.py
```

### 3. Run Complete Part 1 Suite

```bash
# All experiments - runs in ~30-45 minutes
python run_all_part1.py
```

---

## 📊 What Each Experiment Does

| Experiment | Runtime | What It Tests | Key Output |
|------------|---------|---------------|------------|
| **Part 1(a)** | ~30 sec | Single agent baseline | Random walk effectiveness |
| **Part 1(b)** | ~3 min | Agent scaling (R=3-30) | Performance vs agent count |
| **Part 1(c)** | ~5 min | Multi-agent tasks (Tc=3) | Coordination overhead |
| **Part 1(d)** | ~12 min | Multiple tasks, steady-state | Convergence time, statistics |
| **Part 1(e)** | ~8 min | Call-out communication | Swarm intelligence benefit |
| **Part 1(f)** | ~10 min | Call-off improvement | Release mechanism value |

**Total Time: ~40 minutes for complete suite**

---

## 📁 Output Files

After running, check `results/` directory:

```
results/
├── part1a_results.png    # Single agent analysis
├── part1b_results.png    # Agent scaling plots
├── part1c_results.png    # Coordination analysis
├── part1d_results.png    # Steady-state convergence
├── part1e_results.png    # Call-out performance
└── part1f_results.png    # Call-out vs call-off comparison
```

---

## 🎯 Key Results at a Glance

### Performance Progression

```
Random Search:           0.145 tasks/iteration  [Baseline]
    ↓
Call-Out (Rd=400):       0.201 tasks/iteration  [+38%]
    ↓
Call-Off (Rd=400):       0.217 tasks/iteration  [+50%]
```

### Optimal Configurations

**Part 1(b)**: R=30 agents gives best performance for Tc=1
**Part 1(c)**: Need R≥10 for viable Tc=3 operation
**Part 1(d)**: 2000 iterations, 20 runs for robust statistics
**Part 1(e)**: Rd=400 optimal for call-out
**Part 1(f)**: Rd=400 still optimal, but more robust to larger values

---

## 🔬 Experimental Parameters

### Standard Configuration (Parts e-f)

```python
R = 30              # Number of agents
T = 2               # Simultaneous tasks
Tc = 3              # Agents required per task
Tr = 50             # Task radius
Rv = 25             # Agent speed
Rt = 60             # Response duration
Rd = [0...1400]     # Communication range (tested)
Iterations = 2000   # Total (1000 warmup + 1000 measure)
Runs = 20           # For statistical robustness
```

---

## 💡 Understanding the Protocols

### Random Search (Baseline)
```python
Every iteration:
1. Move randomly
2. Check if near task
3. Wait if found
4. Complete when Tc agents present
```
**Performance**: 0.145 tasks/iteration

### Call-Out Protocol
```python
When finding task:
1. Emit signal if need help
2. Nearby agents (within Rd) respond
3. Responders move toward task
4. Response lasts Rt iterations
5. Timeout returns to search
```
**Performance**: 0.201 tasks/iteration (+38%)

### Call-Off Protocol
```python
Call-Out + Release Signal:
1. (Same as call-out 1-4)
2. When task completes: emit call-off
3. All responding agents released immediately
4. Available for new tasks instantly
```
**Performance**: 0.217 tasks/iteration (+50%)

---

## 📈 Interpreting Results

### Plot Types You'll See

**1. Line Plots with Error Bars**
- Show mean performance ± standard deviation
- Compare different configurations
- Identify optimal parameters

**2. Box Plots**
- Show distribution of results across runs
- Reveal variance and outliers
- Assess statistical robustness

**3. Bar Charts**
- Compare absolute improvements
- Highlight relative gains
- Visualize protocol differences

**4. Convergence Plots**
- Track system reaching steady-state
- Show iteration-by-iteration progress
- Determine required warmup period

---

## 🐛 Troubleshooting

### Import Errors

```bash
# Make sure you're in project root
cd sta_assignment

# Check Mesa installation
pip show mesa
# Should show version 2.0.0 or higher

# Reinstall if needed
pip install mesa --upgrade
```

### Plots Don't Show

```bash
# Plots are automatically saved even if display fails
ls results/
# Check for PNG files

# If display needed, ensure matplotlib backend works
python -c "import matplotlib; print(matplotlib.get_backend())"
```

### Slow Performance

```bash
# Reduce runs for testing (edit script)
num_runs = 5  # Instead of 20

# Or reduce iterations
num_iterations = 500  # Instead of 2000

# Note: This affects statistical robustness!
```

---

## 📚 Understanding the Assignment

### Part 1 Structure

**Parts (a-d): Random Benchmark**
- Establish baseline performance
- No communication between agents
- Pure stochastic search
- Analyze steady-state behavior

**Parts (e-f): Swarm Intelligence**
- Add communication protocols
- Test call-out (signal emission)
- Test call-off (release mechanism)
- Compare with random baseline

### Key Questions to Answer

**Part 1(a)**: 
- What's a good movement model? → Uniform random walk
- Is tasks/iteration a good metric? → Yes, when aggregated

**Part 1(d)**:
- How many iterations needed? → 2000 (1000 warmup)
- How many runs needed? → 20 (for <5% error)

**Part 1(e)**:
- Does communication help? → Yes, +38% improvement
- What's optimal Rd? → 400-600

**Part 1(f)**:
- Does call-off improve call-out? → Yes, +8% additional
- Why better? → Eliminates wasted agent-time

---

## 🎓 Learning Objectives

### Concepts Demonstrated

✅ **Agent-Based Modeling**
- Mesa framework usage
- Agent behaviors and interactions
- Environment dynamics

✅ **Swarm Intelligence**
- Local rules → Global behavior
- Emergent coordination
- No central control

✅ **Experimental Design**
- Parameter sweeps
- Statistical validation
- Steady-state analysis

✅ **Performance Analysis**
- Baseline establishment
- Protocol comparison
- Optimization trade-offs

---

## 📝 For Your Report

### Key Points to Include

**Part 1(a)**: 
- Movement model justification
- Metric evaluation
- Baseline characterization

**Part 1(b-c)**:
- Scaling analysis
- Coordination overhead
- Critical thresholds

**Part 1(d)**:
- Convergence analysis
- Statistical methodology
- Benchmark establishment

**Part 1(e)**:
- Communication benefits
- Optimal range selection
- Protocol limitations

**Part 1(f)**:
- Release mechanism value
- Comparative analysis
- Design recommendations

### Suggested Report Structure

```
1. Introduction
   - Problem description
   - Approach overview

2. Methodology
   - Mesa implementation
   - Protocol descriptions
   - Experimental design

3. Results
   - Plots for each part
   - Performance tables
   - Statistical analysis

4. Discussion
   - Protocol comparison
   - Design trade-offs
   - Practical insights

5. Conclusion
   - Key findings
   - Recommendations
   - Future work
```

---

## 🚦 Next Steps

### After Part 1

1. **Review Results**
   - Check all plots in `results/`
   - Understand trends and patterns
   - Note optimal configurations

2. **Prepare Report**
   - Include all plots
   - Explain findings
   - Answer assignment questions

3. **Part 2 Preparation**
   - Read about auction mechanisms
   - Understand game theory basics
   - Consider cost-benefit analysis

### Part 2 Preview

**Game-Theoretic Approach:**
- Implement auction-based coordination
- Agents bid for task participation
- Compare with swarm methods
- Analyze strategic vs. reactive agents

**Key Questions:**
- Does optimization beat swarm intelligence?
- What's the cost of strategic behavior?
- When is each approach better?

---

## 📞 Getting Help

### If Stuck

1. **Check README.md** - Detailed implementation guide
2. **Check PART1_SUMMARY.md** - In-depth analysis (a-d)
3. **Check PART1EF_SUMMARY.md** - Communication protocols (e-f)
4. **Review code comments** - Implementation details explained

### Common Issues

**"Model runs but no improvement"**
- Check use_communication=True for parts e-f
- Verify communication_range > 0
- Ensure use_calloff=True for part f

**"Results don't match expected"**
- Random seed variation is normal
- Check you're using steady-state data only
- Verify warmup period is sufficient

**"Plots look wrong"**
- Ensure matplotlib is installed correctly
- Try saving plots without showing (comment plt.show())
- Check data isn't corrupted (rerun experiment)

---

## ✅ Checklist Before Submission

- [ ] All 6 experiments run successfully
- [ ] All plots generated in `results/`
- [ ] Code runs without errors
- [ ] Results match expected trends
- [ ] Report includes all plots
- [ ] Assignment questions answered
- [ ] Code is commented
- [ ] README included
- [ ] ZIP file contains everything
- [ ] Tested by unzipping and running

---

## 🎉 You're Ready!

Your implementation includes:
- ✅ Complete Mesa-based STA simulation
- ✅ All 6 Part 1 experiments
- ✅ Random, call-out, and call-off protocols
- ✅ Comprehensive analysis and visualization
- ✅ Statistical validation
- ✅ Well-documented code

**Run `python run_all_part1.py` and you're done with Part 1!**

Good luck with Part 2! 🚀