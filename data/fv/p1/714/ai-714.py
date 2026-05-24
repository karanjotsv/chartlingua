import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate a pie chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    json_filepath = Path(json_path)

    if not json_filepath.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
        
    chart_data = config.get('chart_data', [])
    colors = config.get('colors', [])
    
    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=0.5)
        ),
        textposition='auto',
        textinfo='label',
        sort=False,
        direction='clockwise',
        rotation=160 
    ))

    fig.update_traces(
        textfont=dict(
            family="Arial",
            size=16,
            color='black'
        ),
        insidetextorientation='horizontal'
    )
    
    fig.update_layout(
        showlegend=False,
        font=dict(
            family="Arial"
        ),
        margin=dict(t=20, r=20, b=20, l=20),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    output_filename = json_filepath.stem + ".png"
    
    try:
        fig.write_image(output_filename, scale=2, width=600, height=450)
        print(f"Chart successfully saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()