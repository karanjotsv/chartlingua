import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])

# Add first pie chart
pie1_data = chart_data[0]
pie1_text = [f"{label}<br>{value}%" for label, value in zip(pie1_data['labels'], pie1_data['values'])]
fig.add_trace(
    go.Pie(
        labels=pie1_data['labels'],
        values=pie1_data['values'],
        text=pie1_text,
        marker_colors=colors[0]
    ),
    row=1, col=1
)

# Add second pie chart
pie2_data = chart_data[1]
pie2_text = [f"{label}<br>{value}%" for label, value in zip(pie2_data['labels'], pie2_data['values'])]
fig.add_trace(
    go.Pie(
        labels=pie2_data['labels'],
        values=pie2_data['values'],
        text=pie2_text,
        marker_colors=colors[1]
    ),
    row=1, col=2
)

fig.update_traces(
    hoverinfo='label+percent',
    textinfo='text',
    textposition='outside',
    sort=False,
    direction='clockwise',
    insidetextorientation='radial',
    textfont_size=12
)

fig.update_layout(
    annotations=[
        dict(
            text=texts['title_left'],
            x=0.22, y=1.0, font_size=16,
            xref="paper", yref="paper",
            xanchor='center', yanchor='bottom',
            showarrow=False
        ),
        dict(
            text=texts['title_right'],
            x=0.78, y=1.0, font_size=16,
            xref="paper", yref="paper",
            xanchor='center', yanchor='bottom',
            showarrow=False
        )
    ],
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=40, r=40, t=80, b=40),
    paper_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")