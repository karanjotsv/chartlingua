import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    texttemplate="<b>%{label}</b><br>%{value}%",
    textposition='inside',
    insidetextorientation='horizontal',
    insidetextfont=dict(family="Arial", size=14),
    hoverinfo='skip',
    sort=False,
    direction='clockwise',
    rotation=90
)

fig = go.Figure(data=[pie_trace])

# Update layout for styling, title, and annotations
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b><br><span style='color:#555555; font-size:14px;'>{texts.get('subtitle', '')}</span>",
        x=0.01,
        xanchor='left',
        yanchor='top',
        y=0.98,
        font=dict(size=20)
    ),
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(l=20, r=20, t=160, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=-0.1,  # Positioned below the chart area
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color="#555555")
        )
    ]
)

# Generate the output PNG filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)