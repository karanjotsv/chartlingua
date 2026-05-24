import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly, reversing the order to match the original image (top to bottom)
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]
display_texts = [item['display_text'] for item in chart_data][::-1]
annotation_positions = [item['annotation_position'] for item in chart_data][::-1]

# Create a list of colors for the bars, cycling through the provided color list
bar_colors = [colors[i % len(colors)] for i in range(len(chart_data))][::-1]

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=bar_colors,
    hoverinfo='none'
))

# Add data labels next to each bar based on the specified position
for i in range(len(values)):
    if values[i] is not None:
        if annotation_positions[i] == 'inside':
            x_anchor = 'right'
            x_shift = -5
        else:  # 'outside'
            x_anchor = 'left'
            x_shift = 5
        
        fig.add_annotation(
            x=values[i],
            y=categories[i],
            text=display_texts[i],
            showarrow=False,
            xanchor=x_anchor,
            xshift=x_shift,
            font=dict(family="Arial", size=14)
        )

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(size=22, family="Arial")
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        ticksuffix='%',
        domain=[0, 0.95],
        range=[0, 0.026] # Ensure space for outside annotations
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=14)
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.4,
    margin=dict(t=90, b=90, l=120, r=20),
)

# Add source and note annotations at the bottom
fig.add_annotation(
    text=texts.get('source', ''),
    xref="paper", yref="paper",
    x=0, y=-0.12,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12, family="Arial")
)

fig.add_annotation(
    text=texts.get('note', ''),
    xref="paper", yref="paper",
    x=1, y=-0.12,
    xanchor='right', yanchor='top',
    showarrow=False,
    font=dict(size=12, family="Arial")
)

# Determine output filename from the input JSON filename
output_filename = f"{pathlib.Path(json_path).stem}.png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")