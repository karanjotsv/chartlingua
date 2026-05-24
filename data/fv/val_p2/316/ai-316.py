import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    # Use HTML tags for bolding legend items and data point labels
    series_name_bold = f"<b>{series['name']}</b>"
    data_labels_bold = [f"<b>{y}</b>" for y in series['y']]
    
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series_name_bold,
        mode='lines+markers+text',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=6),
        text=data_labels_bold,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=10,
            color='black'
        )
    ))

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title=f"<b>{texts.get('x_axis_title', '')}</b>",
        tickangle=-30,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#BEBEBE'
    ),
    yaxis=dict(
        title=f"<b>{texts.get('y_axis_title', '')}</b>",
        range=[0, 60],
        dtick=5,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#BEBEBE'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial"
    ),
    margin=dict(l=60, r=40, t=100, b=100)
)

# Derive the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")