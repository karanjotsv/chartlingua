import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color=colors.get('bar_color', '#F98D09'),
        line=dict(
            color=colors.get('bar_border_color', '#000000'),
            width=1.5
        )
    ),
    width=0.7,
    hoverinfo='none'
))

# Add annotations inside the bars
for item in chart_data:
    fig.add_annotation(
        x=item['category'],
        y=item['value'] / 2,  # Vertically center the text
        text=item['annotation'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=18,
            color=colors.get('annotation_text_color', '#000000')
        ),
        align="center"
    )

# --- 3. Configure Layout ---
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_color', '#000000'),
        ticks=""
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2.75],
        tickmode='linear',
        tick0=0,
        dtick=0.25,
        showgrid=True,
        gridwidth=1,
        gridcolor=colors.get('grid_color', '#C0C0C0'),
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_color', '#000000'),
        zeroline=False
    ),
    margin=dict(l=60, r=40, t=40, b=40)
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")