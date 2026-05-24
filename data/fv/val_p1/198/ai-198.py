import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Generates a grouped horizontal bar chart from a JSON data file.
    """
    # 1. Argument Parsing
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)
    
    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # 2. JSON Data Loading
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    # 3. Data Extraction from JSON
    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']
    series_names = chart_config['series_names']
    
    # The categories are pre-reversed in the JSON for correct top-to-bottom display in Plotly
    categories = [item['category'] for item in chart_data]

    # 4. Chart Creation
    fig = go.Figure()

    # Add a trace for each data series
    for i, series_name in enumerate(series_names):
        values = [item['values'][i] for item in chart_data]
        fig.add_trace(go.Bar(
            name=series_name,
            y=categories,
            x=values,
            orientation='h',
            marker_color=colors[i]
        ))

    # 5. Layout and Styling
    # Combine title and subtitle
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"
    
    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        barmode='group',
        xaxis={
            'title_text': texts.get('x_axis_title'),
            'showgrid': True,
            'gridcolor': '#E0E0E0',
            'zeroline': False,
            'range': [0, 70]
        },
        yaxis={
            'title_text': texts.get('y_axis_title'),
            'showgrid': False,
            'zeroline': False,
        },
        legend={
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.2,
            'xanchor': 'center',
            'x': 0.5
        },
        font={
            'family': 'Arial',
            'size': 12
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=300, r=30, t=80, b=80) # Left margin for long category labels
    )

    # 6. Output Generation
    output_filename = json_path.with_suffix('.png')
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()