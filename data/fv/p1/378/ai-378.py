import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not pathlib.Path(json_path).is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config["chart_data"]
texts = config["texts"]
colors = config["colors"]

fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# First pie chart
fig.add_trace(go.Pie(
    labels=chart_data[0]['labels'],
    values=chart_data[0]['values'],
    marker_colors=colors[0],
    name=texts['title_1'],
    rotation=90
), 1, 1)

# Second pie chart
fig.add_trace(go.Pie(
    labels=chart_data[1]['labels'],
    values=chart_data[1]['values'],
    marker_colors=colors[1],
    name=texts['title_2'],
    rotation=155
), 1, 2)

fig.update_traces(
    textposition='outside',
    texttemplate='%{label}<br>%{value}%',
    hoverinfo='label+percent',
    hole=0,
    marker_line=dict(color='black', width=1.5),
    showlegend=False,
    textfont=dict(size=12, family="Arial"),
    sort=False
)

fig.update_layout(
    font_family="Arial",
    annotations=[
        dict(text=texts['title_1'], x=0.22, y=1.0, font_size=16, showarrow=False, xanchor='center'),
        dict(text=texts['title_2'], x=0.78, y=1.0, font_size=16, showarrow=False, xanchor='center')
    ],
    margin=dict(t=60, b=20, l=20, r=20),
    paper_bgcolor='white'
)

output_filename_base = pathlib.Path(json_path).stem
fig.write_image(f"{output_filename_base}.png", scale=2, width=900, height=450)

print(f"Chart saved to {output_filename_base}.png")