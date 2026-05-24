import sys
import json
import argparse
import plotly.graph_objects as go
import os

def main():
    # Use argparse for robust command-line argument handling
    parser = argparse.ArgumentParser(description='Generate a chart from a JSON data file.')
    parser.add_argument('json_path', help='The path to the input JSON file.')
    args = parser.parse_args()

    # Ensure the file exists before proceeding
    if not os.path.exists(args.json_path):
        print(f"Error: The file '{args.json_path}' was not found.")
        sys.exit(1)

    # Load data from the specified JSON file
    with open(args.json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    # Extract data, texts, and colors from the loaded JSON
    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    # Prepare data for Plotly
    labels = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        hoverinfo='label+percent',
        textinfo='percent',
        texttemplate='%{value:.1f}%',
        textposition='outside',
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise'
    )])

    # Combine title and subtitle using HTML for formatting
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

    # Update layout for a professional appearance
    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,  # Position legend below the chart
            xanchor="center",
            x=0.5
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        margin=dict(l=60, r=60, t=120, b=120),  # Add margins to prevent clipping
        paper_bgcolor='#E9E9F8',
        plot_bgcolor='#E9E9F8',
        showlegend=True
    )

    # Determine the output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(args.json_path))[0]
    output_filename = f"{base_filename}.png"

    # Write the image file
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == '__main__':
    main()