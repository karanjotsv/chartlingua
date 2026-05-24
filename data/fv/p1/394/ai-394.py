import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error: Could not read or parse the JSON file at {json_path}. Details: {e}")
    sys.exit(1)

chart_data = config['chart_data']
colors = config['colors']
texts = config['texts']

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
text_labels = [f"{d['category']}, {d['value']}, {d['percentage']}%" for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    text=text_labels,
    textinfo='none',
    textposition='outside',
    textfont=dict(family="Arial", size=12),
    hoverinfo='label+percent+value',
    sort=False,
    direction='clockwise',
    rotation=90
))

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=80, r=80, t=50, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")