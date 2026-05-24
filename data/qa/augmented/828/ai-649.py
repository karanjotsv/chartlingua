import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- 2. Create the Chart ---
fig = go.Figure()

# Add the bar trace, ensuring data is plotted in the order it appears in the JSON
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False # Allows text to render outside the plot area if needed
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
else:
    title_text = f"<b>{title_text}</b>" if title_text else ""

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=False,
        ticks='outside',
        tickcolor='lightgrey',
        categoryorder='array', # Explicitly set category order
        categoryarray=x_values
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        showline=False,
        ticks='',
        range=[0, 250]
    ),
    margin=dict(l=70, r=40, t=60, b=100) # Adjust margins to prevent clipping
)

# Add source annotation at the bottom right
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.18, # Position below x-axis
        xanchor='right',
        yanchor='top',
        font=dict(size=10, color="#808080")
    )


# --- 4. Output the Chart ---
# Derive the output filename from the input JSON filename
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")