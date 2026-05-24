import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    categories = [d['category'] for d in data]
    values = [d['value'] for d in data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0],
        name=''
    ))

    fig.update_layout(
        title_text=texts['title'],
        title_x=0.5,
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        font=dict(family="Arial", size=16),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=80, b=60),
        xaxis=dict(
            type='category',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside'
        ),
        yaxis=dict(
            range=[0, 1.5],
            tickvals=[0, 0.5, 1.0, 1.5],
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside'
        )
    )

    fig.add_shape(type="line",
        xref="paper", yref="y",
        x0=0, y0=0.5, x1=1, y1=0.5,
        line=dict(color="grey", width=1)
    )
    fig.add_shape(type="line",
        xref="paper", yref="y",
        x0=0, y0=1.0, x1=1, y1=1.0,
        line=dict(color="grey", width=1)
    )

    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()