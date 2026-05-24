import sys
import json
import plotly.graph_objects as go
import os

# Check if the command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_text = [str(item['value']) for item in chart_data] # Preserve original formatting (int/float)

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=bar_text,
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

# Configure the layout
annotations = []
note_text = texts.get('note')
if note_text:
    annotations.append(
        go.layout.Annotation(
            text=note_text,
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            showarrow=False,
            font=dict(family="Arial", size=12, color="#1f77b4")
        )
    )

source_text = texts.get('source')
if source_text:
    annotations.append(
        go.layout.Annotation(
            text=source_text,
            xref="paper", yref="paper",
            x=1.0, y=-0.2,
            xanchor='right', yanchor='bottom',
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    template='plotly_white',
    font=dict(family="Arial", size=12),
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 600],
        tickvals=[0, 100, 200, 300, 400, 500, 600],
        gridcolor='#e9e9e9'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# Set specific font for bar text to match original
fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")