import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate a chart from a JSON configuration file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    # Get file path from argument
    json_file_path = Path(sys.argv[1])
    if not json_file_path.is_file():
        print(f"Error: File not found at {json_file_path}")
        sys.exit(1)

    # Read JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    # Extract data and texts from config
    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    # Prepare data for Plotly
    labels = [d.get('label', '') for d in chart_data]
    values = [d.get('value', 0) for d in chart_data]
    
    # Create the figure
    fig = go.Figure()

    # Add the pie chart trace
    # Note: Plotly does not support the pseudo-3D perspective of Excel charts.
    # An exploded 2D pie chart is the closest functional representation.
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#444444', width=1) # Adds a subtle border to slices
        ),
        pull=[0.05] * len(values),  # Explode all slices slightly
        texttemplate='%{label}<br>%{value}%',
        textposition='inside',
        textfont=dict(family="Arial"),
        hoverinfo='label+percent',
        sort=False  # Preserve the order from the JSON file
    ))

    # Update layout and styling
    title_text = texts.get('title', '')

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=22)
        ),
        font=dict(family="Arial"),
        showlegend=False,
        margin=dict(t=100, b=30, l=30, r=30),
        paper_bgcolor='#D7E1E8', # Approximates the original background color
        plot_bgcolor='#D7E1E8'
    )
    
    # Derive output filename from the input JSON filename
    output_filename = f"{json_file_path.stem}.png"

    # Write the image file
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()