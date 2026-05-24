import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    fig = go.Figure()

    # Add traces for each data series
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            line=dict(color=colors[i], width=2.5),
            showlegend=False
        ))

    # Add annotations for each line, positioned at the end
    y_anchors = ['middle', 'middle', 'top']
    for i, series in enumerate(chart_data):
        if series.get('x') and series.get('y'):
            fig.add_annotation(
                x=series['x'][-1],
                y=series['y'][-1],
                text=series.get('annotation_text', ''),
                showarrow=False,
                xanchor='left',
                yanchor=y_anchors[i],
                xshift=10,
                align='left',
                font=dict(family="Arial", size=12)
            )

    # Update layout
    fig.update_layout(
        title=dict(
            text=texts.get('title', ''),
            x=0.5,
            xanchor='center',
            font=dict(family="Arial", size=18)
        ),
        xaxis=dict(
            title=texts.get('x_axis_title', ''),
            tickvals=[3, 6, 9, 12],
            range=[-0.5, 14.5],
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title=texts.get('y_axis_title', ''),
            range=[-4.2, 3.2],
            tickvals=[-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
            tickformat='.1f',
            gridcolor='#D3D3D3',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        font=dict(family="Arial"),
        margin=dict(l=80, r=180, t=100, b=80),
        autosize=False,
        width=800,
        height=600
    )

    # Output the image
    output_filename = json_path.with_suffix(".png")
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()