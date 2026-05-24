import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+value+percent',
    textinfo='none',
    sort=False
))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else f"<sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    font=dict(family="Arial", size=12),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=60, b=50),
    legend=dict(
        traceorder='normal'
    )
)

output_filename_base = json_path.stem
output_file = f"{output_filename_base}.png"

fig.write_image(output_file, scale=2)

print(f"Chart successfully generated and saved to {output_file}")