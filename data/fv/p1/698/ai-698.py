import sys
import json
import os
import plotly.graph_objects as go

# Verify that the correct number of command-line arguments is provided.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the specified JSON file exists.
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data structures from the parsed JSON.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly traces.
categories = [d.get('category') for d in chart_data]
values = [d.get('value') for d in chart_data]

# Create the main figure object.
fig = go.Figure()

# Add the bar chart trace.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=[f"{v:,}" for v in values],
    textposition='outside',
    cliponaxis=False  # Allows text to render outside the plot area.
))

# Format the title string using HTML for multi-line support.
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

# Apply comprehensive layout settings.
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        color="white"
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,  # Show Y-axis ticks for scale context.
        tickfont=dict(color='white')
    ),
    margin=dict(t=120, b=80, l=80, r=40),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            align='left',
            font=dict(size=12, color="white")
        )
    ]
)

# Update trace-specific properties like text font.
fig.update_traces(textfont=dict(color='white'))

# Determine the output filename from the input JSON path.
filename_base = os.path.basename(json_path).rsplit('.', 1)[0]
output_filename = f"{filename_base}.png"

# Save the generated chart to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")