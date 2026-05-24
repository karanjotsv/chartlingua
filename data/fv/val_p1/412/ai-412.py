import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data lists
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors,
    marker_line=dict(color='black', width=1),
    text=y_values,
    textposition='inside',
    textfont=dict(family='Arial', size=12, color='black'),
    insidetextanchor='end',
    cliponaxis=False
))

# Build title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        font=dict(family='Arial', size=16, color='black')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(family='Arial', size=12, color='black'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 3.5],
        tick0=0,
        dtick=0.5,
        tickfont=dict(family='Arial', size=12, color='black'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    font=dict(family='Arial', size=12, color='black'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=100, b=80),
    bargap=0.15
)

# Add source annotation if present
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        align='left',
        xanchor='left',
        font=dict(family='Arial', size=10, color='grey')
    )

# Determine output filename and save the image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")