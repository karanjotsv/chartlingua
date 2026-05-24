import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
legend_labels = texts['legend_labels']

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
data_series = {}
for label in legend_labels:
    data_series[label] = [d.get(label) for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add traces based on the series names and their intended chart type
# The order is important for stacking: base layer first, then the next, etc.

# Add "Active Users" trace (Blue, base of the stack)
label_au = "Active Users"
if label_au in legend_labels:
    idx_au = legend_labels.index(label_au)
    fig.add_trace(go.Scatter(
        x=categories,
        y=data_series[label_au],
        name=label_au,
        mode='lines',
        fill='tozeroy',
        stackgroup='one',
        line=dict(width=0, color=colors[idx_au]),
        fillcolor=colors[idx_au]
    ))

# Add "Accounts Created" trace (Green, stacked on top of blue)
label_ac = "Accounts Created"
if label_ac in legend_labels:
    idx_ac = legend_labels.index(label_ac)
    fig.add_trace(go.Scatter(
        x=categories,
        y=data_series[label_ac],
        name=label_ac,
        mode='lines',
        fill='tonexty',
        stackgroup='one',
        line=dict(width=0, color=colors[idx_ac]),
        fillcolor=colors[idx_ac]
    ))

# Add "Unique Visitors" trace (Red, simple line chart)
label_uv = "Unique Visitors"
if label_uv in legend_labels:
    idx_uv = legend_labels.index(label_uv)
    fig.add_trace(go.Scatter(
        x=categories,
        y=data_series[label_uv],
        name=label_uv,
        mode='lines',
        line=dict(color=colors[idx_uv], width=2)
    ))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}" if texts.get('title') else ''

# Update layout for a professional look and feel
fig.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(family="Arial", size=14, color="white"),
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#444444',
        linecolor='white',
        linewidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#444444',
        linecolor='white',
        linewidth=1,
        range=[0, 100],
        tickvals=[0, 20, 40, 60, 80, 100]
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='white',
        borderwidth=0
    ),
    margin=dict(l=80, r=50, t=100, b=80),
    showlegend=True
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")