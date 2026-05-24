import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_file_path = Path(sys.argv[1])

    # Ensure the JSON file exists
    if not json_file_path.is_file():
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)

    # Read the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    # Extract data from the JSON structure
    data = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']

    # Prepare data for Plotly
    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=1)
        ),
        sort=False,
        direction='clockwise',
        textinfo='none',
        hoverinfo='label+percent'
    )

    # Initialize the figure
    fig = go.Figure(data=[pie_trace])

    # Build the title string
    title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Build annotations for the source text
    annotations = []
    if texts.get('source'):
        annotations.append(
            go.layout.Annotation(
                text=texts['source'],
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.25,
                xanchor='left',
                yanchor='bottom'
            )
        )

    # Update the layout
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left'
        ),
        legend=dict(
            x=1,
            y=0.95,
            xanchor='left',
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        paper_bgcolor='#D3D3D3',
        plot_bgcolor='#D3D3D3',
        margin=dict(l=50, r=50, t=80, b=180),
        annotations=annotations,
        showlegend=True
    )

    # Generate the output filename
    output_filename = json_file_path.stem + ".png"

    # Save the chart as a PNG image
    fig.write_image(output_filename, scale=2)

    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()