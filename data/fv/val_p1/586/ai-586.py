import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    textinfo='value',
    textfont=dict(size=12, family="Arial", color='black'),
    hoverinfo='label+percent+value',
    sort=False,
    direction='clockwise',
    rotation=135
))

title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        traceorder='normal'
    ),
    margin=dict(l=40, r=350, t=100, b=40),
    paper_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")