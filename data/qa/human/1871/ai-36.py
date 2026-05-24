import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data points
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=y_values,
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none'
))

# Combine source and notes for the annotation
source_text_parts = [texts.get('source'), texts.get('notes')]
source_text = "<br>".join(filter(None, source_text_parts))

# Update layout
fig.update_layout(
    title=texts.get('title'),
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        range=[min(y_values) - 1, max(y_values) + 1.5]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")