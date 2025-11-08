import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def get_running_average(rates):
    """Calculate the running (cumulative) average."""
    return np.cumsum(rates) / (np.arange(len(rates)) + 1)

def run_part1d():
    """
    Part 1(d): Performance as a function of task number (T)
    - Vary T = 2, 10, 20
    - R = 30, Tc = 3, Tr = 50, Rv = 25
    - Also investigates steady-state and statistical reliability
    """
    
    print("=" * 60)
    print("Part 1(d): Performance as Function of Task Number (T)")
    print("=" * 60)
    
    # Parameters
    task_counts = [2, 10, 20]
    num_agents = 30
    task_radius = 50
    required_agents = 3
    agent_speed = 25
    num_iterations = 2000  # Increased iterations to better see steady state
    num_runs = 10  # Multiple runs for statistical reliability
    
    print(f"\nParameters:")
    print(f"  Task counts (T): {task_counts}")
    print(f"  Number of agents (R): {num_agents}")
    print(f"  Task radius (Tr): {task_radius}")
    print(f"  Required agents per task (Tc): {required_agents}")
    print(f"  Agent speed (Rv): {agent_speed}")
    print(f"  Iterations per run: {num_iterations}")
    print(f"  Number of runs: {num_runs}")
    
    # Store results
    results = {
        'task_counts': task_counts,
        'mean_rates': [],
        'std_rates': [],
        'all_rates': [],
        'steady_state_runs': {} # Store one run for steady-state plot
    }
    
    # Run simulations for each task count
    for num_tasks in task_counts:
        print(f"\n{'='*40}")
        print(f"Running simulations for T = {num_tasks} tasks")
        print(f"{'='*40}")
        
        run_rates = []
        
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents,
                num_tasks=num_tasks,
                task_radius=task_radius,
                required_agents_per_task=required_agents,
                agent_speed=agent_speed,
                seed=42 + run  # Different seed for each run
            )
            
            model.run_model(num_iterations)
            avg_rate = model.get_average_completion_rate()
            run_rates.append(avg_rate)
            
            # Store the first run's detailed completion rate for steady-state analysis
            if run == 0:
                completion_over_time = model.get_completion_rate_over_time()
                results['steady_state_runs'][num_tasks] = completion_over_time
            
            print(f"  Run {run+1}/{num_runs}: {avg_rate:.4f} tasks/iteration")
        
        mean_rate = np.mean(run_rates)
        std_rate = np.std(run_rates)
        
        results['mean_rates'].append(mean_rate)
        results['std_rates'].append(std_rate)
        results['all_rates'].append(run_rates)
        
        print(f"  Mean: {mean_rate:.4f} ± {std_rate:.4f}")
    
    # --- Plotting ---
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Part 1(d) Results: Performance vs. Task Number (R=30, Tc=3)', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Mean performance vs. T (with error bars)
    ax1.errorbar(task_counts, results['mean_rates'], 
                 yerr=results['std_rates'], 
                 marker='o', linewidth=2, markersize=8, capsize=5)
    ax1.set_xlabel('Number of Tasks (T)', fontsize=11)
    ax1.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax1.set_title('Performance vs Number of Tasks', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(task_counts)
    
    # Plot 2: Box plot showing distribution
    box_data = [results['all_rates'][i] for i in range(len(task_counts))]
    ax2.boxplot(box_data, labels=task_counts)
    ax2.set_xlabel('Number of Tasks (T)', fontsize=11)
    ax2.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax2.set_title('Distribution of Performance (10 Runs)', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Steady State Analysis (Running Average)
    for num_tasks in task_counts:
        rates = results['steady_state_runs'][num_tasks]
        running_avg = get_running_average(rates)
        ax3.plot(running_avg, label=f'T={num_tasks}', linewidth=1.5)
    
    ax3.set_xlabel('Iteration', fontsize=11)
    ax3.set_ylabel('Running Average Tasks per Iteration', fontsize=11)
    ax3.set_title('Steady-State Analysis (Single Run)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Total Throughput (Mean Rate * T) - (Optional but interesting)
    # This shows total tasks in system * completion rate
    # Let's plot "Tasks per Agent" instead
    tasks_per_agent = np.array(results['mean_rates']) / num_agents
    ax4.plot(task_counts, tasks_per_agent, marker='^', linewidth=2, 
             markersize=8, color='red')
    ax4.set_xlabel('Number of Tasks (T)', fontsize=11)
    ax4.set_ylabel('Tasks per Iteration per Agent', fontsize=11)
    ax4.set_title('Agent Efficiency vs. Task Load', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(task_counts)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Save plot
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/part1d_results.png', dpi=300, bbox_inches='tight')
    print(f"\n{'='*60}")
    print(f"Plot saved to: results/part1d_results.png")
    plt.show()
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY TABLE (R=30, Tc=3):")
    print("="*60)
    print(f"{'Tasks (T)':<12} {'Mean Rate':<15} {'Std Dev':<15} {'Efficiency':<15}")
    print("-" * 60)
    for i, T in enumerate(task_counts):
        eff = results['mean_rates'][i] / num_agents
        print(f"{T:<12} {results['mean_rates'][i]:<15.4f} "
              f"{results['std_rates'][i]:<15.4f} {eff:<15.4f}")
    
    # Analysis
    print("\n" + "="*60)
    print("ANALYSIS (Part 1d):")
    print("="*60)
    print(f"""
Key Observations:
1. Performance (avg tasks/iteration) increases with more
   simultaneous tasks (T). This is because with more tasks, 
   agents are more likely to stumble upon one during their
   random search. The "search" part of the problem becomes easier.
2. Agent efficiency (tasks per agent) also increases with T.
   This shows that agents are "busier" and more productive
   when more tasks are available.

Steady State Analysis (Plot 3):
- The running average of task completions stabilizes over time.
- For these parameters, the average seems to settle after
  approx 500-1000 iterations. The initial ~200 iterations
  are highly variable (the "warm-up" period).
- Simulating for 1000-2000 iterations seems appropriate to get
  a good measure of the steady-state performance.

Statistical Estimation (Plot 2):
- Running the simulation 10 times gives a good idea of the
  variance in performance (shown by the box plot).
- The variance (and standard deviation) also appears to 
  increase with T. This makes sense, as the complex 
  interactions of 30 agents and 20 tasks can lead to
  more divergent outcomes than with 2 tasks.
- 10 runs seems sufficient for a good statistical estimate,
  though 20 or 30 would be even more robust if time permits.
    """)

if __name__ == "__main__":
    run_part1d()