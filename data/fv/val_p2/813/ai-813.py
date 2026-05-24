import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data_list = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data_list]
values = [d['value'] for d in chart_data_list]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    textinfo='percent',
    insidetextfont=dict(color='white', size=16),
    hoverinfo='label+percent',
    sort=False
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        x=0.5,
        xanchor='center',
        y=-0.1,
        yanchor='top',
        orientation='v'
    ),
    margin=dict(t=140, b=120, l=20, r=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")