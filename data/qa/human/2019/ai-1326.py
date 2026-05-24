import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
output_base_name = Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''

if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = None

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=12, color="#000000"),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    margin=dict(l=80, r=80, t=80, b=80),
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0.01,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10)
    )

output_filename = f"{output_base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")