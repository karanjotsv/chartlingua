import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Generates a chart from a JSON data file using Plotly.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Derive base filename from the JSON file path
    filename_base = os.path.basename(json_file_path).rsplit('.', 1)[0]

    # Load data from the specified JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        sys.exit(1)

    # Extract data for the chart
    data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    # Prepare data for Plotly Pie chart
    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]

    # Create the pie chart trace
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        textinfo='label',
        textfont=dict(color='white', size=16, family='Arial'),
        textposition='inside',
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise'
    ))

    # --- Layout Configuration ---
    
    # Construct title and subtitle string
    title_parts = []
    if texts.get('title'):
        title_parts.append(f"<b style='font-size: 1.2em;'>{texts['title']}</b>")
    if texts.get('subtitle'):
        title_parts.append(f"<span style='font-size: 0.9em;'>{texts['subtitle']}</span>")
    full_title = "<br>".join(title_parts)

    # Configure layout properties
    fig.update_layout(
        title_text=full_title if full_title else None,
        title_x=0.5,
        title_y=0.95,
        paper_bgcolor='black',
        plot_bgcolor='black',
        showlegend=False,
        margin=dict(t=40, b=40, l=40, r=40),
        font=dict(family="Arial", color="white")
    )

    # Add source/note as an annotation if present
    annotations = []
    if texts.get('source'):
        annotations.append(
            dict(
                xref='paper', yref='paper',
                x=0, y=-0.05,
                xanchor='left', yanchor='top',
                text=texts['source'],
                showarrow=False,
                align='left',
                font=dict(size=12, color="#cccccc")
            )
        )
    if annotations:
        fig.update_layout(annotations=annotations)

    # --- Output ---

    # Define the output image filename
    output_filename = f"{filename_base}.png"

    # Save the chart as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()