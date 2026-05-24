import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# --- Chart Generation ---

# Extract data for plotting
categories = [item['category'] for item in chart_data['chart_data']]
series_names = chart_data['series_names']
colors = chart_data['colors']
texts = chart_data['texts']

# Create a figure
fig = go.Figure()

# Add a bar trace for each series
for i, series_name in enumerate(series_names):
    values = [item['values'][i] for item in chart_data['chart_data']]
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series_name,
        marker_color=colors[i]
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickangle=-90,
        title_font=dict(size=16),
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 140],
        dtick=20,
        title_font=dict(size=16),
        tickfont=dict(size=12),
        gridcolor='darkgrey'
    ),
    barmode='group',
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="right",
        x=0.98,
        bgcolor='rgba(255, 255, 255, 0.5)'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='#EAEAEA',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=100, b=180) # Increased bottom margin for rotated labels
)

# Add border to the plotting area
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

# --- Output ---

# Derive the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")