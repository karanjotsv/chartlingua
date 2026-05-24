import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    rotation=90,
    textinfo='percent',
    textposition='outside',
    textfont_size=14,
    hoverinfo='label+percent'
))

title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.75,
        y=0.75,
        xanchor='left',
        yanchor='top',
        bordercolor="Black",
        borderwidth=1
    ),
    margin=dict(l=50, r=50, t=100, b=50),
    paper_bgcolor='white',
    showlegend=True
)

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")