import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
# The lists are reversed to ensure the chart is displayed top-to-bottom as in the original image
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text from being clipped at the chart's edge
))

# Update layout to match the original chart's appearance
fig.update_layout(
    title_text=texts.get('title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=40, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, 150]  # Set range to provide space for text labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#808080')
        )
    ]
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")