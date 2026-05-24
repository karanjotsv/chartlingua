import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
labels = [f"{item['category']} {item['value']}%" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#A9A9A9', width=1.5)
    ),
    hoverinfo='none',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=152.5 # Position the red/green divide vertically
))

# Update layout for a professional look
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=28,
            color="black"
        )
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.9,
        font=dict(
            family="Arial",
            size=16
        ),
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    margin=dict(l=40, r=200, t=100, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)