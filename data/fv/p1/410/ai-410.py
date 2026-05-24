import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Main function to generate a pie chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    # Extract data and texts from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        sort=False,  # Preserve the order from the JSON file
        direction='counterclockwise',
        texttemplate='%{value:.1f}%',
        textposition='outside',
        hoverinfo='label+percent',
        insidetextorientation='radial'
    )

    fig = go.Figure(data=[pie_trace])

    # Combine title and subtitle using HTML tags
    title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

    # Update layout for a professional appearance
    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        title_font=dict(
            family="Arial",
            size=24
        ),
        font=dict(
            family="Arial",
            size=14,
            color="black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=140, b=120),
        paper_bgcolor='#F0F0FF',
        plot_bgcolor='#F0F0FF'
    )
    
    # Determine the output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a high-resolution PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()