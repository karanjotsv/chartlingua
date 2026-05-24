import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)


chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    width=0.6
))

max_value = 0
max_index = -1
if values:
    max_value = max(values)
    max_index = values.index(max_value)

if max_index != -1:
    fig.add_annotation(
        x=categories[max_index],
        y=values[max_index],
        text=str(values[max_index]),
        showarrow=False,
        font=dict(family="Arial", size=12, color='black'),
        yshift=10
    )

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    yaxis=dict(
        range=[0, 50],
        tickmode='linear',
        tick0=0,
        dtick=5,
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1
    ),
    xaxis=dict(
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80),
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")