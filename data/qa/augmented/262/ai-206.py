import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the output filename from the input JSON path
output_filename = json_file_path.rsplit('.', 1)[0] + '.png'

# Load data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.2f}' for v in values],
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False # Ensures text labels are not cut off at the top
))

# Combine title and subtitle using HTML formatting
title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
if title_text and subtitle_text:
    combined_title = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
else:
    combined_title = title_text or subtitle_text

# Update layout
fig.update_layout(
    title={
        'text': combined_title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=categories,
        ticktext=categories
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        range=[0, 60],
        dtick=10
    ),
    margin=dict(l=80, r=20, t=80, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Generate and save the image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")