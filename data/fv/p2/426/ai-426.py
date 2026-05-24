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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])

for i in range(num_series):
    y_values = [item['values'][i] for item in chart_data]
    error_values = [item['errors'][i] for item in chart_data]
    
    trace = go.Bar(
        name=texts['legend_labels'][i],
        x=categories,
        y=y_values,
        marker_color=colors[i],
        error_y=dict(type='data', array=error_values, visible=True, color='black', thickness=1.5)
    )
    
    if i == 0:  # Special styling for the first bar series (DMFT)
        trace.marker.line.color = 'black'
        trace.marker.line.width = 1.5

    fig.add_trace(trace)

fig.update_layout(
    barmode='group',
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=18, color="black"),
    legend=dict(
        x=0.02,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,1)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=18)
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 80],
        gridcolor='black',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    margin=dict(l=100, r=20, t=20, b=80)
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")