import sys
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [str(item['category']) for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    showlegend=False,
    hoverinfo='none'
))

# --- 3. Configure Layout ---
# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += f"<i>{subtitle_text}</i>"

# Combine source/note for annotations
source_text = texts.get('source')
annotations = []
if source_text:
    annotations.append(
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.1,  # Adjust y to position below x-axis
            xanchor='left', yanchor='top',
            align='left'
        )
    )

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',  # Treat numeric labels as discrete categories
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 4.2],
        tickvals=[0, 1, 2, 3, 4],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    showlegend=False,
    margin=dict(l=50, r=30, t=50, b=50),
    annotations=annotations
)

# --- 4. Output the Image ---
# Derive output filename from JSON path
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

# Save the figure as a high-resolution PNG
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)