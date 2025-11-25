"""
Error Rate Analysis for Financial Retrieval QA Dataset

This script calculates error rates for each chatbot in the dataset and outputs
a JSON report. Error rate is defined as: (number of rows with errors) / (total number of rows)

A row has an error if the 'error' column is not NaN (i.e., contains a value 1-5).
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime


def calculate_error_rates(csv_path='train.csv'):
    """
    Calculate error rates for each chatbot in the dataset.
    
    Parameters:
    -----------
    csv_path : str
        Path to the CSV file containing the dataset
        
    Returns:
    --------
    tuple: (summary_df, df)
        summary_df: DataFrame with error rate summary per chatbot
        df: Full dataset DataFrame
    """
    # Load the dataset
    df = pd.read_csv(csv_path)
    
    # Calculate error rates per chatbot
    results = []
    
    for chatbot in df['chatbot'].unique():
        chatbot_data = df[df['chatbot'] == chatbot]
        total_rows = len(chatbot_data)
        
        # Count rows with errors (error column is not NaN)
        # Using pd.notna() to check for non-null values
        rows_with_errors = chatbot_data['error'].notna().sum()
        
        # Calculate error rate
        error_rate = (rows_with_errors / total_rows) * 100 if total_rows > 0 else 0
        
        # Calculate accuracy (complement of error rate)
        accuracy = ((total_rows - rows_with_errors) / total_rows) * 100 if total_rows > 0 else 0
        
        results.append({
            'chatbot': chatbot,
            'total_questions': int(total_rows),
            'errors': int(rows_with_errors),
            'correct': int(total_rows - rows_with_errors),
            'error_rate_percent': round(error_rate, 2),
            'accuracy_percent': round(accuracy, 2)
        })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    summary_df = summary_df.sort_values('error_rate_percent', ascending=False)
    
    return summary_df, df


def analyze_error_types(df):
    """
    Analyze error types distribution per chatbot.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Full dataset DataFrame
        
    Returns:
    --------
    dict
        Dictionary containing error type distribution per chatbot
    """
    # Filter to rows with errors
    error_data = df[df['error'].notna()].copy()
    
    if len(error_data) == 0:
        return {}
    
    # Error type mapping
    error_types = {
        1: "Fiscal vs Calendar Period Confusion",
        2: "Period Shift",
        3: "Rounding / Formatting",
        4: "Ambiguous Interpretation",
        5: "Non-Answer / Refusal"
    }
    
    # Create error type column
    error_data['error_type'] = error_data['error'].map(error_types)
    
    # Create pivot table
    error_pivot = pd.crosstab(error_data['chatbot'], error_data['error_type'], margins=False)
    
    # Convert to dictionary format
    error_distribution = {}
    for chatbot in error_pivot.index:
        error_distribution[chatbot] = {}
        for error_type in error_pivot.columns:
            count = int(error_pivot.loc[chatbot, error_type])
            if count > 0:
                error_distribution[chatbot][error_type] = count
    
    return error_distribution


def generate_json_report(summary_df, df, output_file='error_rate_report.json'):
    """
    Generate a comprehensive JSON report with error rate analysis.
    
    Parameters:
    -----------
    summary_df : pd.DataFrame
        DataFrame containing error rate summary per chatbot
    df : pd.DataFrame
        Full dataset DataFrame
    output_file : str
        Path to output JSON file
    """
    # Get error type distribution
    error_distribution = analyze_error_types(df)
    
    # Calculate statistics
    best_chatbot = summary_df.loc[summary_df['error_rate_percent'].idxmin()]
    worst_chatbot = summary_df.loc[summary_df['error_rate_percent'].idxmax()]
    
    # Build report structure
    report = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_rows_in_dataset': int(len(df)),
            'total_chatbots': int(len(summary_df)),
            'chatbots_analyzed': sorted(df['chatbot'].unique().tolist())
        },
        'summary': {
            'chatbots': summary_df.to_dict('records'),
            'statistics': {
                'best_performing': {
                    'chatbot': best_chatbot['chatbot'],
                    'error_rate_percent': float(best_chatbot['error_rate_percent']),
                    'accuracy_percent': float(best_chatbot['accuracy_percent']),
                    'total_questions': int(best_chatbot['total_questions']),
                    'errors': int(best_chatbot['errors']),
                    'correct': int(best_chatbot['correct'])
                },
                'worst_performing': {
                    'chatbot': worst_chatbot['chatbot'],
                    'error_rate_percent': float(worst_chatbot['error_rate_percent']),
                    'accuracy_percent': float(worst_chatbot['accuracy_percent']),
                    'total_questions': int(worst_chatbot['total_questions']),
                    'errors': int(worst_chatbot['errors']),
                    'correct': int(worst_chatbot['correct'])
                },
                'average_error_rate_percent': float(summary_df['error_rate_percent'].mean()),
                'average_accuracy_percent': float(summary_df['accuracy_percent'].mean()),
                'total_questions_across_all_chatbots': int(summary_df['total_questions'].sum()),
                'total_errors_across_all_chatbots': int(summary_df['errors'].sum()),
                'total_correct_across_all_chatbots': int(summary_df['correct'].sum())
            }
        },
        'error_type_distribution': error_distribution,
        'error_type_descriptions': {
            '1': 'Fiscal vs Calendar Period Confusion',
            '2': 'Period Shift',
            '3': 'Rounding / Formatting',
            '4': 'Ambiguous Interpretation',
            '5': 'Non-Answer / Refusal'
        }
    }
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report


if __name__ == "__main__":
    # Calculate error rates
    summary_df, full_df = calculate_error_rates('train.csv')
    
    # Generate JSON report
    output_file = 'error_rate_report.json'
    report = generate_json_report(summary_df, full_df, output_file)
    
    print(f"JSON report generated successfully: {output_file}")

