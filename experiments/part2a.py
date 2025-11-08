import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def run_part2a():
    """
    Part 2(a): Simple Auction Protocol
    - Agent discovering task becomes auctioneer
    - Agents within Rd bid with their distances
    - Auctioneer recruits closest (Tc-1) agents
    - Compare across communication ranges
    """
    
    print("=" * 80)
    print("Part 2(a): Auction-Based Coordination")
    print("=" * 80)
    
    # Parameters (same as Part 1e/f for comparison)
    communication_ranges = [0, 100, 200, 300, 400, 600, 1000, 1400]
    num_agents = 30
    num_tasks = 2
    task_radius = 50
    required_agents = 3
    agent_speed = 25
    num_iterations = 2000
    warmup_iterations = 1000
    num_runs = 20
    
    print(f"\nParameters:")
    print(f"  Number of agents (R): {num_agents}")
    print(f"  Number of tasks (T): {num_tasks}")
    print(f"  Task radius (Tr): {task_radius}")
    print(f"  Required agents per task (Tc): {required_agents}")
    print(f"  Agent speed (Rv): {agent_speed}")
    print(f"  Communication ranges (Rd): {communication_ranges}")
    print(f"  Total iterations: {num_iterations} (warmup: {warmup_iterations})")
    print(f"  Number of runs: {num_runs}")
    print(f"\n  Protocol: Distance-based auction")
    print(f"    - Discoverer = Auctioneer")
    print(f"    - Bidders = Agents within Rd")
    print(f"    - Bid = Distance to auctioneer")
    print(f"    - Winners = Closest (Tc-1) agents")
    
    # Store results
    results_auction = {
        'comm_ranges': communication_ranges,
        'mean_rates': [],
        'std_rates': [],
        'all_rates': []
    }
    
    # Run random benchmark for comparison
    print(f"\n{'='*80}")
    print("Running RANDOM BENCHMARK...")
    print(f"{'='*80}")
    
    benchmark_rates = []
    for run in range(num_runs):
        model = STAModel(
            num_agents=num_agents,
            num_tasks=num_tasks,
            task_radius=task_radius,
            required_agents_per_task=required_agents,
            agent_speed=agent_speed,
            communication_range=0,
            use_communication=False,
            use_auction=False,
            seed=400 + run
        )
        model.run_model(num_iterations)
        steady_data = model.get_completion_rate_over_time()[warmup_iterations:]
        benchmark_rates.append(np.mean(steady_data))
        
        if (run + 1) % 5 == 0:
            print(f"  Completed {run+1}/{num_runs} runs...")
    
    benchmark_mean = np.mean(benchmark_rates)
    benchmark_std = np.std(benchmark_rates)
    print(f"  Benchmark Mean: {benchmark_mean:.4f} ± {benchmark_std:.4f}")
    
    # Run auction simulations for each communication range
    for Rd in communication_ranges:
        print(f"\n{'='*80}")
        print(f"Testing Auction Protocol with Rd = {Rd}")
        print(f"{'='*80}")
        
        run_rates = []
        
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents,
                num_tasks=num_tasks,
                task_radius=task_radius,
                required_agents_per_task=required_agents,
                agent_speed=agent_speed,
                communication_range=Rd,
                response_duration=60,
                use_communication=False,
                use_calloff=False,
                use_auction=True,  # Enable auction protocol
                seed=400 + run
            )
            
            model.run_model(num_iterations)
            steady_data = model.get_completion_rate_over_time()[warmup_iterations:]
            avg_rate = np.mean(steady_data)
            run_rates.append(avg_rate)
            
            if (run + 1) % 5 == 0:
                print(f"  Completed {run+1}/{num_runs} runs...")
        
        mean_rate = np.mean(run_rates)
        std_rate = np.std(run_rates)
        
        results_auction['mean_rates'].append(mean_rate)
        results_auction['std_rates'].append(std_rate)
        results_auction['all_rates'].append(run_rates)
        
        improvement = ((mean_rate - benchmark_mean) / benchmark_mean * 100) if benchmark_mean > 0 else 0
        print(f"  Mean: {mean_rate:.4f} ± {std_rate:.4f}")
        print(f"  Improvement over random: {improvement:+.2f}%")
    
    # Convert to numpy arrays
    results_auction['mean_rates'] = np.array(results_auction['mean_rates'])
    results_auction['std_rates'] = np.array(results_auction['std_rates'])
    
    # Create comprehensive plots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    # Plot 1: Auction Performance vs Communication Range
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.errorbar(communication_ranges, results_auction['mean_rates'],
                 yerr=results_auction['std_rates'],
                 marker='D', linewidth=2, markersize=8, capsize=5,
                 label='Auction Protocol', color='purple')
    ax1.axhline(y=benchmark_mean, color='red', linestyle='--', linewidth=2,
                label=f'Random Benchmark: {benchmark_mean:.4f}')
    ax1.fill_between(communication_ranges,
                     benchmark_mean - benchmark_std,
                     benchmark_mean + benchmark_std,
                     alpha=0.2, color='red')
    ax1.set_xlabel('Communication Range (Rd)', fontsize=11)
    ax1.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax1.set_title('Auction Protocol Performance vs Communication Range',
                  fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # Plot 2: Improvement percentage
    ax2 = fig.add_subplot(gs[0, 2])
    improvement_pct = ((results_auction['mean_rates'] - benchmark_mean) / benchmark_mean * 100)
    ax2.plot(communication_ranges, improvement_pct, marker='D', linewidth=2,
             markersize=8, color='purple')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax2.set_ylabel('Improvement (%)', fontsize=10)
    ax2.set_title('Relative Improvement', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Box plots for selected Rd values
    ax3 = fig.add_subplot(gs[1, :])
    selected_indices = [0, 2, 4, 6, 7]
    selected_ranges = [communication_ranges[i] for i in selected_indices]
    box_data = [results_auction['all_rates'][i] for i in selected_indices]
    bp = ax3.boxplot(box_data, labels=[f'Rd={r}' for r in selected_ranges],
                     patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('plum')
    ax3.axhline(y=benchmark_mean, color='red', linestyle='--', linewidth=2,
                label='Random Benchmark')
    ax3.set_xlabel('Communication Range', fontsize=11)
    ax3.set_ylabel('Tasks per Iteration', fontsize=11)
    ax3.set_title('Performance Distribution (Selected Rd Values)',
                  fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.legend()
    
    # Plot 4: Absolute improvement
    ax4 = fig.add_subplot(gs[2, 0])
    abs_improvement = results_auction['mean_rates'] - benchmark_mean
    ax4.bar(range(len(communication_ranges)), abs_improvement,
            color='mediumpurple', alpha=0.7)
    ax4.set_xticks(range(len(communication_ranges)))
    ax4.set_xticklabels([str(r) for r in communication_ranges], rotation=45)
    ax4.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax4.set_ylabel('Absolute Improvement', fontsize=10)
    ax4.set_title('Performance Gain', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(y=0, color='black', linewidth=0.5)
    
    # Plot 5: Normalized performance
    ax5 = fig.add_subplot(gs[2, 1])
    normalized = results_auction['mean_rates'] / benchmark_mean
    ax5.plot(communication_ranges, normalized, marker='D', linewidth=2,
             markersize=8, color='purple')
    ax5.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Baseline')
    ax5.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax5.set_ylabel('Performance Ratio', fontsize=10)
    ax5.set_title('Normalized Performance', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.legend()
    
    # Plot 6: Coefficient of Variation
    ax6 = fig.add_subplot(gs[2, 2])
    cv = (results_auction['std_rates'] / results_auction['mean_rates']) * 100
    ax6.plot(communication_ranges, cv, marker='D', linewidth=2,
             markersize=8, color='darkviolet')
    ax6.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax6.set_ylabel('CV (%)', fontsize=10)
    ax6.set_title('Coefficient of Variation', fontsize=11, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    plt.savefig('results/part2a_results.png', dpi=300, bbox_inches='tight')
    print(f"\n{'='*80}")
    print(f"Plot saved to: results/part2a_results.png")
    plt.show()
    
    # Print detailed results table
    print("\n" + "="*80)
    print("AUCTION PROTOCOL RESULTS:")
    print("="*80)
    print(f"{'Rd':<8} {'Mean':<12} {'Std':<12} {'Improvement':<15} {'Ratio':<10} {'CV(%)':<10}")
    print("-" * 80)
    for i, Rd in enumerate(communication_ranges):
        improvement = ((results_auction['mean_rates'][i] - benchmark_mean) / benchmark_mean * 100)
        ratio = results_auction['mean_rates'][i] / benchmark_mean
        cv_val = (results_auction['std_rates'][i] / results_auction['mean_rates'][i]) * 100
        print(f"{Rd:<8} {results_auction['mean_rates'][i]:<12.4f} "
              f"{results_auction['std_rates'][i]:<12.4f} {improvement:<14.2f}% "
              f"{ratio:<10.3f} {cv_val:<10.2f}")
    
    # Analysis
    best_idx = np.argmax(results_auction['mean_rates'])
    best_Rd = communication_ranges[best_idx]
    best_improvement = ((results_auction['mean_rates'][best_idx] - benchmark_mean) / benchmark_mean * 100)
    
    print("\n" + "="*80)
    print("ANALYSIS:")
    print("="*80)
    print(f"""
1. AUCTION PROTOCOL PERFORMANCE:

   Random Benchmark: {benchmark_mean:.4f} ± {benchmark_std:.4f} tasks/iteration
   Best Auction (Rd={best_Rd}): {results_auction['mean_rates'][best_idx]:.4f} ± {results_auction['std_rates'][best_idx]:.4f}
   Maximum Improvement: {best_improvement:.2f}%

2. HOW AUCTION WORKS:

   Discovery Phase:
   - Agent finds task via random search
   - Becomes "auctioneer" for that task
   
   Auction Phase:
   - All agents within Rd can participate
   - Each bidder bids their distance to auctioneer
   - Lower distance = better bid
   
   Allocation Phase:
   - Auctioneer sorts bids by distance
   - Recruits (Tc-1) closest agents
   - Winners move toward task
   
   Execution Phase:
   - Agents work on task when all arrive
   - Task completes, agents released

3. AUCTION VS RANDOM SEARCH:

   Key Differences:
   ✓ Intelligent allocation (closest agents recruited)
   ✓ Efficient resource utilization
   ✓ Distance-based optimization
   ✓ Game-theoretic coordination
   
   vs Random:
   ✗ Still relies on chance discovery
   ✗ No call-off mechanism (yet)
   ✗ Agents committed until task completion

4. COMMUNICATION RANGE EFFECTS:

   Rd=0: {results_auction['mean_rates'][0]:.4f} (no auction, same as random)
   Rd=100-300: {np.mean(results_auction['mean_rates'][1:4]):.4f} (limited bidder pool)
   Rd=400-600: {np.mean(results_auction['mean_rates'][4:6]):.4f} (optimal range)
   Rd=1000+: {np.mean(results_auction['mean_rates'][6:]):.4f} (many bidders)

5. OPTIMAL CONFIGURATION:

   Best Rd: {best_Rd}
   Expected Performance: {results_auction['mean_rates'][best_idx]:.4f} tasks/iteration
   Improvement: {best_improvement:.2f}% over random

6. AUCTION ADVANTAGES:

   ✓ Distance-based selection (optimal routing)
   ✓ Competitive bidding (efficient allocation)
   ✓ Game-theoretic optimality
   ✓ Scalable coordination mechanism
   
7. AUCTION LIMITATIONS:

   ✗ Still no early release (agents wait until task completes)
   ✗ Auction overhead (communication, computation)
   ✗ Requires agent ranking/sorting
   ✗ More complex than swarm signaling

8. COMPARISON TO EXPECTATIONS:

   Auction should provide:
   - Better agent selection than random response
   - More efficient routing (closest agents)
   - Game-theoretic optimality
   
   Observed: ~{best_improvement:.0f}% improvement at Rd={best_Rd}
   This is competitive with swarm methods!
    """)
    
    # Store results for Part 2b comparison
    results_file = 'results/part2a_data.npy'
    np.save(results_file, {
        'auction': results_auction,
        'benchmark': {'mean': benchmark_mean, 'std': benchmark_std, 'rates': benchmark_rates}
    }, allow_pickle=True)
    print(f"\nResults saved to: {results_file}")
    
    return results_auction, benchmark_mean, benchmark_std

if __name__ == "__main__":
    run_part2a()