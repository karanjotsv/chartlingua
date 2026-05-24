import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = "<br>".join(part for part in title_parts if part)

source_parts = [texts.get('source'), texts.get('notes')]
source_text = "<br>".join(part for part in source_parts if part)

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=100, b=120),
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 70],
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False
    )
)

if source_text:
    fig.add_annotation(
        showarrow=False,
        text=source_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.25,
        xanchor='left',
        yanchor='bottom',
        align='left'
    )

output_filename_base = json_file_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")