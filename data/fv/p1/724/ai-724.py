import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
custom_text = [f"{d['label']}<br>{d['value']:,}" for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = f"<b>{texts.get('title', '')}</b>" if texts.get('title') else None

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(t=100, b=80, l=100, r=100),
    paper_bgcolor='white',
    plot_bgcolor='white',
    autosize=False,
    width=800,
    height=650
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")