import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors[0] if len(colors) > 0 else None,
        line=dict(
            color=colors[1] if len(colors) > 1 else '#000000',
            width=1
        )
    ),
    showlegend=False
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle using HTML for flexible styling
title_text_parts = []
if texts.get('title'):
    title_text_parts.append(f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_text_parts.append(f"<span style='font-size: 16px;'>{texts['subtitle']}</span>")
combined_title = "<br>".join(title_text_parts)

fig.update_layout(
    title=dict(
        text=combined_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    width=800,
    height=500,
    margin=dict(l=90, r=40, t=50, b=80),
    bargap=0.15,
    xaxis=dict(
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        tickmode='auto',
        ticks='outside',
        showgrid=False
    ),
    yaxis=dict(
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        range=[0, 300000],
        tickmode='linear',
        dtick=50000,
        gridcolor='#CCCCCC',
        gridwidth=1
    )
)

# --- 4. Output the Figure ---
# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")