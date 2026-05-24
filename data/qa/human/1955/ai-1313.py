import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
output_path = os.path.splitext(json_path)[0] + ".png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    texttemplate="%{label} %{value}%",
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title_text=full_title if full_title else None,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=14),
    margin=dict(l=80, r=80, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=0.01,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color="grey")
    )

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")