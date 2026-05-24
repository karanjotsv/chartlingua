import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the JSON object
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly; reverse to display from top to bottom
categories = [d['category'] for d in data][::-1]
values = [d['value'] for d in data][::-1]

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
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    ),
    # Clip text inside the plot area if it overflows
    cliponaxis=False
))

# Build title string from JSON
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Build annotations for source/notes
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='#666666')
        )
    )

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font_family='Arial',
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        showline=False,
        showticklabels=True,
        side='bottom',
        tickfont=dict(size=12),
        title_font=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=180, r=40, t=40, b=80),
    annotations=annotations
)

# Set x-axis range to prevent data labels from being clipped
max_value = max(values) if values else 0
fig.update_xaxes(range=[0, max_value * 1.15], tickmode='linear', dtick=50)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)