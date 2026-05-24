import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']
    
    categories = chart_data['categories']
    series_data = chart_data['series']

    fig = go.Figure()

    for i, series in enumerate(series_data):
        fig.add_trace(go.Bar(
            x=categories,
            y=series.get('data', []),
            name=series.get('name', ''),
            marker_color=colors[i]
        ))

    fig.update_layout(
        barmode='stack',
        title=dict(
            text=texts.get('title'),
            x=0.5,
            y=0.95,
            font=dict(size=18)
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_label'),
            showgrid=False,
            showline=True,
            linecolor='grey',
            ticks='outside'
        ),
        yaxis=dict(
            title=dict(
                text=texts.get('y_axis_label'),
                font=dict(size=16)
            ),
            range=[0, 4500],
            tickmode='linear',
            dtick=500,
            gridcolor='#D3D3D3',
            showline=True,
            linecolor='grey',
            ticks='outside'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            traceorder="normal"
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=90, r=40, t=80, b=120)
    )

    output_filename = json_path.with_suffix('.png')

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Wrapping the script logic in a main function for clarity, but avoiding complex structures.
    main()