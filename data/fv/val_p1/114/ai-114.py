import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    fig = go.Figure()

    series_list = chart_data.get('chart_data', {}).get('series', [])
    colors = chart_data.get('colors', [])

    for i, series in enumerate(series_list):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=1.5)
        ))

    texts = chart_data.get('texts', {})
    
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Arial", color='white'),
        title_text=texts.get('title'),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=True,
            gridcolor='#555555',
            showticklabels=False,
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='#555555',
            showticklabels=False,
            zeroline=False,
            showline=False
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.7,
            xanchor="right",
            x=0.98,
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        autosize=False,
        width=800,
        height=600
    )

    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()