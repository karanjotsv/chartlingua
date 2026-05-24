import sys
import json
import os
import plotly.graph_objects as go

# This script requires a command-line argument for the JSON file path.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists before proceeding.
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data and configuration from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON.
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly trace.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the bar trace to the figure.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update the layout for a professional and accurate appearance.
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12),
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],  # Extend range to accommodate text above the highest bar.
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        linecolor='black'
    ),
    # Use an annotation for the source line to position it accurately.
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.22,  # Positioned below the x-axis labels.
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Derive the output filename from the input JSON filename.
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")