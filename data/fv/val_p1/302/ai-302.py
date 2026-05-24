import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Generates a chart from a JSON data file provided via command-line argument.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # Load data from JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    # Extract data for plotting
    data = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']

    labels = [d['category'] for d in data]
    values = [d['value'] for d in data]

    # Create the pie chart trace
    # The original is a 3D pie chart, which is not a standard Plotly chart type.
    # We will create a standard 2D pie chart to represent the data accurately.
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        texttemplate='%{label}<br>%{value}%',
        textposition='outside',
        hole=0,
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise'
    )])

    # Update layout
    title_text_parts = []
    if texts.get('title'):
        title_text_parts.append(texts['title'])
    if texts.get('subtitle'):
        title_text_parts.append(f'<span style="font-size: 14px;">{texts["subtitle"]}</span>')
    
    title_text = "<br>".join(title_text_parts)

    fig.update_layout(
        title_text=title_text if title_text else None,
        title_x=0.5,
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.7,
            xanchor="right",
            x=1.2
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=80, r=200, t=50, b=50) # Increased right margin for legend
    )

    # Add source/note as annotation
    annotation_text_parts = []
    if texts.get('source'):
        annotation_text_parts.append(texts['source'])
    if texts.get('note'):
        annotation_text_parts.append(texts['note'])
        
    annotation_text = "<br>".join(annotation_text_parts)

    if annotation_text:
        fig.add_annotation(
            text=annotation_text,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top'
        )

    # Generate output filename from JSON path
    output_filename = json_path.with_suffix('.png').name
    
    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()