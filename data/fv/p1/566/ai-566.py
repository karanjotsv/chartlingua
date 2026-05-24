import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_for_slices = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_for_slices,
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='#333333', width=0.5)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=False,
    margin=dict(t=100, b=50, l=100, r=100),
    paper_bgcolor='white',
    plot_bgcolor='white',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    insidetextorientation='radial'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")