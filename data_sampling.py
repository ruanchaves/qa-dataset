"""
Data Sampling for Quality Review

This script extracts a random sample of 50 Q&A pairs balanced across the top 25
most common categories from train.csv and writes them to a JSON file.
"""

import pandas as pd
import json
import random
from datetime import datetime


def sample_qa_pairs(csv_path='train.csv', output_file='qa_sample.json', n_samples=50, n_categories=25):
    """
    Extract a random sample of Q&A pairs balanced across the top N categories.
    
    Parameters:
    -----------
    csv_path : str
        Path to the CSV file containing the dataset
    output_file : str
        Path to output JSON file
    n_samples : int
        Total number of samples to extract (default: 50)
    n_categories : int
        Number of top categories to use (default: 25)
    """
    # Load the dataset
    df = pd.read_csv(csv_path)
    
    # Get unique Q&A pairs (one row per question-gt_answer combination)
    # We'll use the first occurrence of each unique question-gt_answer pair
    unique_qa = df[['question', 'gt_answer', 'category']].drop_duplicates(subset=['question', 'gt_answer'])
    
    # Get top N most common categories
    category_counts = unique_qa['category'].value_counts()
    top_categories = category_counts.head(n_categories).index.tolist()
    
    print(f"Top {n_categories} categories:")
    for i, cat in enumerate(top_categories, 1):
        count = category_counts[cat]
        print(f"  {i}. {cat}: {count} unique Q&A pairs")
    
    # Calculate samples per category (balanced distribution)
    samples_per_category = n_samples // n_categories
    remainder = n_samples % n_categories
    
    # Sample from each category
    sampled_pairs = []
    random.seed(42)  # For reproducibility
    
    for i, category in enumerate(top_categories):
        # Get all Q&A pairs for this category
        category_data = unique_qa[unique_qa['category'] == category]
        
        # Determine how many samples to take from this category
        # Distribute remainder samples across first few categories
        n_samples_cat = samples_per_category + (1 if i < remainder else 0)
        
        # Sample from this category
        if len(category_data) >= n_samples_cat:
            sampled = category_data.sample(n=n_samples_cat, random_state=42)
        else:
            # If category has fewer pairs than needed, take all available
            sampled = category_data
            print(f"Warning: Category '{category}' has only {len(category_data)} unique Q&A pairs, "
                  f"taking all available (requested {n_samples_cat})")
        
        sampled_pairs.append(sampled)
    
    # Combine all sampled pairs
    final_sample = pd.concat(sampled_pairs, ignore_index=True)
    
    # Shuffle the final sample to mix categories
    final_sample = final_sample.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Convert to list of dictionaries for JSON output
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_samples': len(final_sample),
            'total_categories': len(top_categories),
            'samples_per_category': samples_per_category,
            'categories_included': top_categories,
            'source_file': csv_path
        },
        'samples': []
    }
    
    for idx, row in final_sample.iterrows():
        output_data['samples'].append({
            'sample_id': idx + 1,
            'category': row['category'],
            'question': row['question'],
            'golden_answer': row['gt_answer']
        })
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully sampled {len(final_sample)} Q&A pairs")
    print(f"Output written to: {output_file}")
    
    # Print summary by category
    print("\nSample distribution by category:")
    category_dist = final_sample['category'].value_counts().sort_index()
    for cat, count in category_dist.items():
        print(f"  {cat}: {count} samples")
    
    return output_data


if __name__ == "__main__":
    # Extract sample
    sample_data = sample_qa_pairs('train.csv', 'qa_sample.json', n_samples=50, n_categories=25)
    
    print("\nSampling complete!")

