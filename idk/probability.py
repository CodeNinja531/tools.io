import random
import pandas as pd

def run_simulation(num_trials):
    """
    Simulates the game for a given number of trials and records the outcome counts 
    for the four possible game-ending scenarios.
    Box: 2 White (W), 2 Yellow (Y), 3 Red (R). Game ends on W or Y. Boy draws first.
    """
    box = ['W', 'W', 'Y', 'Y', 'R', 'R', 'R']
    
    # Dictionary to store the counts for each scenario: (Player, Ball)
    scenario_counts = {
        ('Boy', 'W'): 0,
        ('Boy', 'Y'): 0,
        ('Girl', 'W'): 0, # <-- This is the target case
        ('Girl', 'Y'): 0,
    }
    
    for _ in range(num_trials):
        turn = 1
        
        while True:
            player = "Boy" if turn % 2 != 0 else "Girl"
            ball = random.choice(box)
            
            # Check if the game ends (W or Y drawn)
            if ball in ['W', 'Y']:
                scenario_counts[(player, ball)] += 1
                break # Game over for this trial

            # If a red ball (R) was drawn, the game continues
            turn += 1

    return scenario_counts

def display_results(scenario_counts, num_trials):
    """Formats and prints the simulation results with highlighting for the target case."""
    
    data = []
    for (player, ball), count in scenario_counts.items():
        
        probability = count / num_trials
        is_target = (player == 'Girl' and ball == 'W')
        
        # Add visual indicator for the target case
        scenario_name = f"{player} draws {ball}" if is_target else f"{player} draws {ball}"
        
        data.append({
            'Game Ending Scenario': scenario_name,
            'No. of Cases (Count)': f"{count:,}",  # Format with thousands separator
            'Empirical Probability': f"{probability:.4f}",
            'Sort_Order': 0 if is_target else 1 # Used for sorting the target case to the top
        })

    df_results = pd.DataFrame(data)
    
    # Sort and clean up the DataFrame
    df_results = df_results.sort_values(by=['Sort_Order', 'Game Ending Scenario'], ascending=[True, True])
    df_results = df_results.drop(columns=['Sort_Order'])
    
    # Print the table and summary
    print(f"Monte Carlo Simulation Results (Total Trials: {num_trials:,})\n")
    print(df_results.to_string(index=False))

    target_count = scenario_counts[('Girl', 'W')]
    target_prob = target_count / num_trials
    
    print("\n" + "="*50)
    print("✨ Probability of Target Case")
    print("="*50)
    print(f"The number of times the Girl drew a White ball was: {target_count:,}")
    print(f"Empirical Probability: {target_count:,} / {num_trials:,} = {target_prob:.4f}")
    print(f"(Theoretical Probability: 0.15 or 3/20)")
    print("="*50)


# --- User Control: Set the number of trials here ---
NUM_TRIALS = 1000
# ----------------------------------------------------

# Run the simulation and display the results
counts = run_simulation(NUM_TRIALS)
display_results(counts, NUM_TRIALS)