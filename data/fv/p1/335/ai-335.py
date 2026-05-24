import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces (bars) to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        font=dict(family="Arial", size=28, color='black'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickmode='array',
        tickvals=[str(year) for year in chart_data[0]['x']],
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 15000000],
        dtick=2500000,
        tickformat=',.0f',
        gridcolor='white'
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.2,
    margin=dict(l=100, r=20, t=100, b=80)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")