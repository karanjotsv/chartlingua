import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file at {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file at {json_path} is not a valid JSON.")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format the text to match the original chart's "Label – Value%" style.
custom_text = [f"{item['label']} – {item['value']:.2f}%" for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent'
))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    margin=dict(t=100, b=40, l=40, r=40),
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")