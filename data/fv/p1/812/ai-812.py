import sys
import json
import plotly.graph_objects as go
import math

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = json_path.split('/')[-1].rsplit('.', 1)[0]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 2. Prepare Data for Plotting ---
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 3. Create Pie Chart Trace ---
trace = go.Pie(
    labels=labels,
    values=values,
    marker={
        'colors': colors,
        'line': {'color': 'white', 'width': 3}
    },
    textinfo='percent',
    textfont={'color': 'white', 'size': 22},
    insidetextorientation='horizontal',
    hoverinfo='label+percent',
    sort=False,
    direction='counterclockwise',
    rotation=90  # Start the first slice (Coast Guard) at the 12 o'clock position
)

# --- 4. Create Annotations for External Labels ---
annotations = []
total_value = sum(values)
# Start angle for annotations (90 degrees is 12 o'clock)
current_angle_deg = 90
label_radius = 1.25 # Distance of labels from the center of the pie

for i, item in enumerate(chart_data):
    slice_angle_deg = (item['value'] / total_value) * 360
    # Calculate the midpoint angle of the slice for label placement
    mid_angle_deg = current_angle_deg - (slice_angle_deg / 2)
    mid_angle_rad = math.radians(mid_angle_deg)

    x_pos = label_radius * math.cos(mid_angle_rad)
    y_pos = label_radius * math.sin(mid_angle_rad)

    annotations.append(
        go.layout.Annotation(
            x=x_pos,
            y=y_pos,
            text=f"<b>{item['label']}</b>",
            showarrow=False,
            font=dict(
                family="Arial",
                size=16,
                color=colors[i]
            ),
            xanchor='center',
            yanchor='middle'
        )
    )
    # Update the angle for the next slice
    current_angle_deg -= slice_angle_deg

# --- 5. Configure Layout ---
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

layout = go.Layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font={'family': "Arial", 'color': 'white'},
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin={'l': 40, 'r': 40, 't': 120, 'b': 40},
    annotations=annotations,
    # Define a square aspect ratio and range to position annotations correctly
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False, range=[-1.6, 1.6]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False, range=[-1.6, 1.6], scaleanchor="x", scaleratio=1)
)

# --- 6. Generate and Save Chart ---
fig = go.Figure(data=[trace], layout=layout)
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")