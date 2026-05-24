import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Generates a pie chart from a JSON data file.
    Usage: python <script_name>.py <path_to_json_file>
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_file_path = Path(sys.argv[1])
    if not json_file_path.is_file():
        print(f"Error: File not found at {json_file_path}")
        sys.exit(1)
        
    output_image_path = json_file_path.with_suffix('.png')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_spec = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    chart_data = chart_spec.get('chart_data', [])
    texts = chart_spec.get('texts', {})
    colors = chart_spec.get('colors', [])

    labels = [item.get('category', '') for item in chart_data]
    values = [item.get('value', 0) for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=1)),
        hoverinfo='label+percent',
        textinfo='none',
        texttemplate='%{label} %{value}%',
        textposition='outside',
        sort=False,
        direction='counterclockwise',
        rotation=90
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(l=100, r=100, t=40, b=50),
        font=dict(family="Arial", size=14, color="#000000"),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    
    annotations = []
    if texts.get('source'):
        annotations.append(
            dict(
                text=texts['source'],
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.0,
                y=0,
                xanchor='right',
                yanchor='bottom',
                font=dict(size=12)
            )
        )
    
    if annotations:
        fig.update_layout(annotations=annotations)

    try:
        fig.write_image(output_image_path, scale=2)
        print(f"Chart successfully saved to {output_image_path}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()