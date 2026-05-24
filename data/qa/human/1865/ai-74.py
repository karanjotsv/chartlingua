import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
    
# Derive output filename from JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=90  # Start the first slice at the top (12 o'clock)
))

# Update layout
fig.update_layout(
    showlegend=False,
    font=dict(family="Arial", size=12),
    margin=dict(l=40, r=40, t=40, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts['source'],
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            align="right",
            font=dict(
                size=10,
                color="#666666"
            )
        )
    ]
)

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")