import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

categories = [item['category'] for item in data]
num_series = len(texts['legend_labels'])
series_data = [[item['values'][i] for item in data] for i in range(num_series)]

for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i]
    ))

fig.update_layout(
    barmode='group',
    font=dict(family="Arial"),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=200),
    xaxis=dict(
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='grey'
    ),
    yaxis=dict(
        range=[0, 70],
        dtick=10,
        showline=True,
        linewidth=1,
        linecolor='grey',
        gridcolor='LightGray'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.65,
        xanchor="center",
        x=0.5
    )
)

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")