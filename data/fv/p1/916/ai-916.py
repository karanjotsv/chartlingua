import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create figure
fig = go.Figure()

# Add data series traces
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(
            color=colors[i],
            width=2,
            dash=series['line_style'],
            shape='spline', 
            smoothing=1.3
        ),
        hoverinfo='none',
        showlegend=False
    ))

# Add annotations from the JSON file
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        font=dict(family="Arial", size=14, color="black"),
        align=ann['align']
    )

# Add custom x-axis ticks and labels
for tick in texts.get('x_axis_ticks', []):
    fig.add_shape(type="line",
        x0=tick['x'], y0=-35, x1=tick['x'], y1=-38,
        line=dict(color="black", width=2)
    )
    fig.add_annotation(
        x=tick['x'],
        y=-40,
        text=f"<b>{tick['label']}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color="black"),
        yanchor="top"
    )

# Add custom axis lines and titles
fig.add_shape(type="line", x0=0, y0=-38, x1=100, y1=-38, line=dict(color="black", width=2)) # X-axis
fig.add_shape(type="line", x0=0, y0=-35, x1=0, y1=50, line=dict(color="black", width=2)) # Y-axis

# Axis arrows
fig.add_annotation(x=100, y=-38, ax=98, ay=-38, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')
fig.add_annotation(x=0, y=50, ax=0, ay=48, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')

# Y-axis direction arrow and labels
fig.add_shape(type="line", x0=-5, y0=-25, x1=-5, y1=40, line=dict(color="black", width=1.5))
fig.add_annotation(x=-5, y=40, ax=-5, ay=38, showarrow=True, arrowhead=2, arrowsize=1.5)
fig.add_annotation(x=-5, y=-25, ax=-5, ay=-23, showarrow=True, arrowhead=2, arrowsize=1.5)

fig.add_annotation(x=-7, y=45, text=texts['y_axis_labels']['endothermique'], showarrow=False, font=dict(family="Arial", size=14, color="black"), xanchor="right")
fig.add_annotation(x=-7, y=-30, text=texts['y_axis_labels']['exothermique'], showarrow=False, font=dict(family="Arial", size=14, color="black"), xanchor="right")

# Surfusion indicator
fig.add_shape(type="line", x0=65, y0=-42, x1=75, y1=-42, line=dict(color="black", width=1.5))
fig.add_annotation(x=65, y=-42, ax=67, ay=-42, showarrow=True, arrowhead=2, arrowsize=1.5)
fig.add_annotation(x=75, y=-42, ax=73, ay=-42, showarrow=True, arrowhead=2, arrowsize=1.5)

# Axis titles
fig.add_annotation(x=105, y=-38, text=f"<b>{texts['x_axis_title']}</b>", showarrow=False, font=dict(family="Arial", size=16), xanchor="left", yanchor="middle")
fig.add_annotation(x=0, y=58, text=f"<b>{texts['y_axis_title']}</b>", showarrow=False, font=dict(family="Arial", size=16), xanchor="center", yanchor="top")

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        visible=False,
        range=[-15, 110]
    ),
    yaxis=dict(
        visible=False,
        range=[-50, 60]
    ),
    margin=dict(l=50, r=50, t=50, b=50),
    showlegend=False
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")