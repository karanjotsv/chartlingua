import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Generates a Plotly chart from a JSON data file provided via command-line argument.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart figure
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        textinfo='percent',
        textposition='outside',
        sort=False,
        direction='clockwise',
        rotation=90  # Start the first slice at the top
    )])

    # Update layout for a professional appearance
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=100, b=120, l=40, r=40),
        paper_bgcolor='#EAEAF7',
        showlegend=True
    )

    # Determine output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart successfully generated and saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()