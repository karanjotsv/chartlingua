import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the chart data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.2f}' for v in values],
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,  # Prevents text labels from being clipped
    textfont=dict(family="Arial", size=12, color='black')
))

# Configure the layout
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.22,
            xanchor='left', yanchor='bottom',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0073e6")
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.22,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", color='black'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-30,
        showgrid=False,
        linecolor='lightgrey',
        tickfont=dict(family="Arial", size=12, color='grey')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 18],
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1,
        tickfont=dict(family="Arial", size=12, color='grey')
    ),
    showlegend=False,
    margin=dict(t=50, b=120, l=80, r=40),
    annotations=annotations
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")