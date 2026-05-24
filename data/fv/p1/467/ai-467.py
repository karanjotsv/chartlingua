import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Initialize figure
fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=chart_data['colors'][i])
    ))

# Combine title and subtitle for the main title
title_parts = []
if chart_data['texts'].get('title'):
    title_parts.append(chart_data['texts']['title'])
if chart_data['texts'].get('subtitle'):
    title_parts.append(f"<br><sup>{chart_data['texts']['subtitle']}</sup>")
final_title = "".join(title_parts) if title_parts else None


# Update layout
fig.update_layout(
    title_text=final_title,
    yaxis_title_text=chart_data['texts']['y_axis_title'],
    xaxis_title_text=chart_data['texts']['x_axis_title'],
    font=dict(
        family="Arial",
        size=14
    ),
    xaxis=dict(
        range=[1980, 2025],
        tickmode='linear',
        tick0=1980,
        dtick=5,
        showgrid=True,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        range=[0, 100],
        tickmode='linear',
        tick0=0,
        dtick=25,
        showgrid=True,
        gridcolor='lightgray'
    ),
    plot_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=80, r=40, t=40, b=40)
)

# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")