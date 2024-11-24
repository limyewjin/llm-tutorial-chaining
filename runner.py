import api
import checker
from datetime import datetime
import csv
import time
from statistics import mean, median, stdev
from typing import Literal

def run_chain(model_name: Literal["gemini", "anthropic", "openai"]) -> dict:
    """Run a single chain for the specified model."""
    print(f"Running {model_name}")
    ask_func = getattr(api, f"ask_{model_name}")
    
    # Initial request
    initial_list = ask_func('Name ten words as you can that end with "can". Return as a list with each word on a new line labeled by 1., 2., and so on.')
    print(f"Initial list:\n{initial_list}")
    initial_count = checker.check_wordlist(initial_list)
    
    # Chained request
    prompt = f"""
    Here are ten words that end with "can":
    {initial_list}

    Replace all words that do not end with "can" or are not real words with real words that end with "can". Place your thinking in <thinking> tag.

    Finally, return as a new list with only the replaced words (or original if correct) on a new line labeled by 1., 2., and so on.
    """.strip()
    
    chained_list = ask_func(prompt)
    print(f"Chained list:\n{chained_list}")
    chained_count = checker.check_wordlist(chained_list)
    
    return {
        'model': model_name,
        'initial_list': initial_list,
        'initial_count': initial_count,
        'chained_list': chained_list,
        'chained_count': chained_count,
        'improvement': chained_count - initial_count
    }

def run_comparison(iterations: int = 10, delay: float = 1.0):
    """Run comparison across all models multiple times."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = []
    models = ["gemini", "anthropic", "openai"]
    
    # Run tests
    with open(f'model_comparison_{timestamp}.csv', 'w', newline='') as csvfile:
        fieldnames = ['iteration', 'model', 'initial_list', 'initial_count', 
                     'chained_list', 'chained_count', 'improvement']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(iterations):
            print(f"Running iteration {i+1}/{iterations}")
            for model in models:
                try:
                    result = run_chain(model)
                    result['iteration'] = i + 1
                    results.append(result)
                    writer.writerow(result)
                    time.sleep(delay)
                except Exception as e:
                    print(f"Error with {model} on iteration {i+1}: {str(e)}")
    
    # Calculate statistics per model
    stats = {}
    for model in models:
        model_results = [r for r in results if r['model'] == model]
        if model_results:
            initial_counts = [r['initial_count'] for r in model_results]
            chained_counts = [r['chained_count'] for r in model_results]
            improvements = [r['improvement'] for r in model_results]
            
            stats[model] = {
                'count': len(model_results),
                'avg_initial': mean(initial_counts),
                'avg_chained': mean(chained_counts),
                'avg_improvement': mean(improvements),
                'median_improvement': median(improvements),
                'std_improvement': stdev(improvements) if len(improvements) > 1 else 0
            }
    
    # Write statistics
    with open(f'model_stats_{timestamp}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['model', 'metric', 'value'])
        for model, model_stats in stats.items():
            for metric, value in model_stats.items():
                writer.writerow([model, metric, f"{value:.2f}" if isinstance(value, float) else value])
    
    return results, stats

if __name__ == "__main__":
    results, stats = run_comparison(iterations=10, delay=1.0)
    
    print("\nResults Summary:")
    for model, model_stats in stats.items():
        print(f"\n{model.upper()}:")
        for metric, value in model_stats.items():
            print(f"  {metric}: {value:.2f}" if isinstance(value, float) else f"  {metric}: {value}")
