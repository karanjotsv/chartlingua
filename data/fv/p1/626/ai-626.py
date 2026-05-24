import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate the chart from a JSON config file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    output_filename = json_path.with_suffix('.png')

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(
                color=colors[i % len(colors)],
                dash=series.get('line_style', 'solid'),
                width=2
            )
        ))

    annotations = []
    if texts.get('source_left'):
        annotations.append(
            dict(
                text=texts['source_left'],
                showarrow=False,
                xref="paper", yref="paper",
                x=0.0, y=-0.25,
                xanchor='left', yanchor='top',
                align='left',
                font=dict(size=10)
            )
        )
    if texts.get('source_right'):
        annotations.append(
            dict(
                text=texts['source_right'],
                showarrow=False,
                xref="paper", yref="paper",
                x=1.0, y=-0.25,
                xanchor='right', yanchor='top',
                align='right',
                font=dict(size=10)
            )
        )

    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            font=dict(size=28),
            x=0.05,
            xanchor='left',
            y=0.95,
            yanchor='top'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showticklabels=False,
            ticks='',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showticklabels=False,
            ticks='',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='black'
        ),
        xaxis_title_font_size=24,
        yaxis_title_font_size=24,
        font=dict(family="Arial"),
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            x=1.02,
            y=0.85,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0,
            font=dict(size=20)
        ),
        margin=dict(l=120, r=200, t=100, b=150),
        annotations=annotations
    )

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()