import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python your_script_name.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Explode all slices except the first (largest) one to match the original chart's style
pull_values = [0] * len(values)
if len(values) > 1:
    pull_values = [0] + [0.3] * (len(values) - 1)

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=1)
    ),
    pull=pull_values,
    textinfo='value',
    texttemplate='%{value:,}',
    textposition='outside',
    rotation=150,
    sort=False  # Preserve the order from the JSON file
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.05
    ),
    margin=dict(l=40, r=200, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)