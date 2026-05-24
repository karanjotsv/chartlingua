import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

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
    rotation=90,
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0, 0.7])
))

fig.update_layout(
    title_text=texts['title'],
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        x=0.75,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        borderwidth=1,
        bordercolor='black',
        font=dict(size=14)
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=40, r=40, t=100, b=40),
    width=800,
    height=550
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)