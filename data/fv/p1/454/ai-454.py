import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

chart_data = chart_spec.get('chart_data', [])
colors = chart_spec.get('colors', [])
texts = chart_spec.get('texts', {})

for i, series in enumerate(chart_data):
    line_style = series.get('line', {})
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=colors[i % len(colors)],
            dash=line_style.get('dash', 'solid'),
            width=line_style.get('width', 2)
        )
    ))

fig.update_layout(
    title_text=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    margin=dict(l=60, r=20, t=30, b=50)
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")