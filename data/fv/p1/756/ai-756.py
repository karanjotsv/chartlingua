import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        marker_color=colors[i % len(colors)] if colors else None
    ))

title_text = texts.get('title') if texts.get('title') else ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    barmode='stack',
    title_text=title_text if title_text else None,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis_range=[0, 60],
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=50, b=180)
)

fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside'
)

fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    gridcolor='lightgrey',
    ticks='outside'
)

if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0, y=-0.6,
        xanchor='left', yanchor='bottom',
        showarrow=False,
        font=dict(size=10)
    )

output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")