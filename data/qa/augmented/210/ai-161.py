import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#1f77b4'),
    text=[f"{v:,}".replace(",", " ") for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevent text labels from being clipped
))

# Build title string from JSON
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
elif title_text:
    full_title = title_text
else:
    full_title = None

# Update layout for a professional look
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        ticks='outside',
        tickformat=',',
        range=[0, max(values) * 1.1] # Ensure space for outside text
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Display categories from top to bottom
        showgrid=False,
        ticks=''
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=60, t=50, b=80),  # Adjust margins for labels and source text
    showlegend=False,
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color="#666666"
            )
        )
    ]
)

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")