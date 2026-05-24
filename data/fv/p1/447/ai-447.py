import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

texts = chart_data['texts']
data = chart_data['chart_data']
colors = chart_data['colors']

fig = make_subplots(
    rows=2, cols=3,
    specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}],
           [{'type': 'bar', 'colspan': 3}, None, None]],
    subplot_titles=texts['subplot_titles']
)

# Pie Chart (a)
pie_a_colors = [colors.get(label, '#CCCCCC') for label in data['pie_a']['labels']]
fig.add_trace(go.Pie(
    labels=data['pie_a']['labels'],
    values=data['pie_a']['values'],
    marker=dict(colors=pie_a_colors, line=dict(color='#000000', width=1)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    sort=False,
    direction='clockwise',
    rotation=120,
    showlegend=False
), row=1, col=1)

# Pie Chart (b)
pie_b_colors = [colors.get(label, '#CCCCCC') for label in data['pie_b']['labels']]
fig.add_trace(go.Pie(
    labels=data['pie_b']['labels'],
    values=data['pie_b']['values'],
    marker=dict(colors=pie_b_colors, line=dict(color='#000000', width=1)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    sort=False,
    direction='clockwise',
    rotation=125,
    showlegend=False
), row=1, col=2)

# Pie Chart (c)
pie_c_colors = [colors.get(label, '#CCCCCC') for label in data['pie_c']['labels']]
fig.add_trace(go.Pie(
    labels=data['pie_c']['labels'],
    values=data['pie_c']['values'],
    marker=dict(colors=pie_c_colors, line=dict(color='#000000', width=1)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    sort=False,
    direction='clockwise',
    rotation=125,
    showlegend=False
), row=1, col=3)

# Bar Chart (d)
bar_d_colors = [colors.get(label, '#CCCCCC') for label in data['bar_d']['categories']]
fig.add_trace(go.Bar(
    x=data['bar_d']['categories'],
    y=data['bar_d']['values'],
    marker=dict(color=bar_d_colors, line=dict(color='#000000', width=1)),
    showlegend=False
), row=2, col=1)

fig.update_layout(
    title_text=texts['main_title'],
    title_x=0.5,
    font_family="Arial",
    width=1100,
    height=800,
    margin=dict(t=100, b=150, l=40, r=40),
    plot_bgcolor='white',
    showlegend=False
)

fig.add_annotation(
    text=texts['bar_chart_description'],
    xref="paper", yref="paper",
    x=0.5, y=-0.1,
    showarrow=False,
    align="center",
    font=dict(size=12, family="Arial")
)

fig.update_yaxes(
    range=[0, 6],
    tickvals=[0, 2, 4, 6],
    showgrid=True,
    gridcolor='lightgray',
    gridwidth=1,
    zeroline=False,
    row=2, col=1
)
fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    row=2, col=1
)

output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")