import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print(f"Error: Could not read or parse the JSON file at '{json_file_path}'.")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=colors[i]
    ))

fig.update_layout(
    barmode='group',
    title=dict(
        text=texts['title'],
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    xaxis=dict(
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[0, 80]
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=1
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=30, t=80, b=180)
)

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_file = f"{base_name}.png"

fig.write_image(output_image_file, scale=2)

print(f"Chart saved to {output_image_file}")