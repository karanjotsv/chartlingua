import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,
    direction='clockwise',
    rotation=105,
    textinfo='none',
    hoverinfo='label+percent'
))

title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    legend=dict(
        x=0.8,
        y=0.9,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=100, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_png_path = f"{base_filename}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")