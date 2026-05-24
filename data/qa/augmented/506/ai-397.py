import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Data is visually ordered top-to-bottom, so reverse for Plotly's bottom-to-top y-axis
chart_data.reverse()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(f"{int(v)}%")
    else:
        text_labels.append(f"{v}%")

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickformat='%{x}%',
        range=[0, 14]
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
    ),
    margin=dict(l=100, r=40, t=30, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")