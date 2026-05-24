import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [d['label'] for d in data]
values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    textinfo='none',
    hoverinfo='label+percent',
    direction='counterclockwise'
))

title_text = texts.get('title', '')

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    font_family="Arial",
    font_size=16,
    legend=dict(
        traceorder='normal',
        x=0.85,
        y=0.9,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)'
    ),
    paper_bgcolor='#F0F0F0',
    plot_bgcolor='#F0F0F0',
    margin=dict(l=40, r=40, t=80, b=40),
    width=800,
    height=500
)

output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")