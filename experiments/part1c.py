import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def run_part1c():
    """
    Part 1(c): Performance vs. Agent Number with Tc=3
    - Vary R = 3, 5, 10, 20, 30
    - T = 1, Tc = 3, Tr = 50, Rv = 25
    """
    
    print("=" * 60)
    print("Part 1(c): Performance as Function of Agent Number (Tc=3)")
    print("=" * 60)
    
    # Parameters
    agent_counts = [3, 5, 10, 20, 30]
    num_tasks = 1
    task_radius = 50
    required_agents = 3  # This is the change from Part 1(b)
    agent_speed = 25
    num_iterations = 1000
    num_runs = 10  # Multiple runs for statistical reliability
    
    print(f"\nParameters:")
    print(f"  Agent counts (R): {agent_counts}")
    print(f"  Number of tasks (T): {num_tasks}")
    print(f"  Task radius (Tr): {task_radius}")
    print(f"  Required agents per task (Tc): {required_agents}")
    print(f"  Agent speed (Rv): {agent_speed}")
    print(f"  Iterations per run: {num_iterations}")
    print(f"  Number of runs: {num_runs}")
    
    # Store results
    results = {
        'agent_counts': agent_counts,
        'mean_rates': [],
        'std_rates': [],
        'all_rates': []
    }
    
    # Run simulations for each agent count
    for num_agents in agent_counts:
        print(f"\n{'='*40}")
        print(f"Running simulations for R = {num_agents} agents")
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
            
            print(f"  Run {run+1}/{num_runs}: {avg_rate:.4f} tasks/iteration")
        
        mean_rate = np.mean(run_rates)
        std_rate = np.std(run_rates)
        
        results['mean_rates'].append(mean_rate)
        results['std_rates'].append(std_rate)
        results['all_rates'].append(run_rates)
        
        print(f"  Mean: {mean_rate:.4f} ± {std_rate:.4f}")
    
    # Convert to numpy arrays for plotting
    results['mean_rates'] = np.array(results['mean_rates'])
    results['std_rates'] = np.array(results['std_rates'])
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Part 1(c) Results: Performance vs. Agent Number (Tc=3)', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Mean performance with error bars
    ax1.errorbar(agent_counts, results['mean_rates'], 
                 yerr=results['std_rates'], 
                 marker='o', linewidth=2, markersize=8, capsize=5)
    ax1.set_xlabel('Number of Agents (R)', fontsize=11)
    ax1.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax1.set_title('Performance vs Number of Agents (with std dev)', 
                  fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(agent_counts)
    
    # Plot 2: Box plot showing distribution
    box_data = [results['all_rates'][i] for i in range(len(agent_counts))]
    ax2.boxplot(box_data, labels=agent_counts)
    ax2.set_xlabel('Number of Agents (R)', fontsize=11)
    ax2.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax2.set_title('Distribution of Performance', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Performance improvement ratio (normalized to R=3)
    # Avoid division by zero if baseline is 0
    baseline = results['mean_rates'][0]
    if baseline > 0:
        normalized = results['mean_rates'] / baseline
        ax3.plot(agent_counts, normalized, marker='s', linewidth=2, 
                 markersize=8, color='green')
        ax3.axhline(y=1, color='r', linestyle='--', alpha=0.5)
        ax3.set_ylabel('Performance Ratio (relative to R=3)', fontsize=11)
    else:
        ax3.text(0.5, 0.5, 'Baseline (R=3) rate is 0,\n'
                          'cannot show relative improvement.',
                 ha='center', va='center', transform=ax3.transAxes)
        
    ax3.set_xlabel('Number of Agents (R)', fontsize=11)
    ax3.set_title('Normalized Performance Improvement', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(agent_counts)

    # Plot 4: Efficiency (tasks per agent)
    efficiency = results['mean_rates'] / np.array(agent_counts)
    ax4.plot(agent_counts, efficiency, marker='^', linewidth=2, 
             markersize=8, color='red')
    ax4.set_xlabel('Number of Agents (R)', fontsize=11)
    ax4.set_ylabel('Tasks per Iteration per Agent', fontsize=11)
    ax4.set_title('Agent Efficiency', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(agent_counts)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Save plot
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/part1c_results.png', dpi=300, bbox_inches='tight')
    print(f"\n{'='*60}")
    print(f"Plot saved to: results/part1c_results.png")
    plt.show()
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY TABLE (Tc=3):")
    print("="*60)
    print(f"{'Agents (R)':<12} {'Mean Rate':<15} {'Std Dev':<15} {'Efficiency':<15}")
    print("-" * 60)
    for i, R in enumerate(agent_counts):
        eff = results['mean_rates'][i] / R
        print(f"{R:<12} {results['mean_rates'][i]:<15.4f} "
              f"{results['std_rates'][i]:<15.4f} {eff:<15.4f}")
    
    # Analysis
    print("\n" + "="*60)
    print("ANALYSIS (Tc=3):")
    print("="*60)
    print(f"""
Key Observations:
1. Performance is significantly lower than in Part 1(b) because 3 
   agents (Tc=3) are required to complete a task, not just 1.
2. When R=3, it is extremely difficult for all 3 agents to be
   in the task radius simultaneously by chance. Performance may be near 0.
3. As R increases, the probability of 3 agents being in the 
   task radius (Tr=50) increases, leading to a rise in performance.
4. Agent efficiency (per-agent) is much lower and also exhibits
   diminishing returns, as many agents are "wasted" searching
   when only 3 are needed at the task.
    """)

if __name__ == "__main__":
    run_part1c()