import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
colors = chart_config.get('colors', [])
texts = chart_config.get('texts', {})

values = [d['value'] for d in chart_data]
hover_labels = [d['category'] for d in chart_data]
text_labels = [d['label'] for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=hover_labels,
    values=values,
    text=text_labels,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,
    direction='clockwise',
    rotation=180
)])

fig.update_traces(
    textposition='inside',
    textfont=dict(family="Arial", color='black', size=24),
    insidetextorientation='horizontal'
)

fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font_family="Arial",
    margin=dict(l=20, r=20, t=20, b=20)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")