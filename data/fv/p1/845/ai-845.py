import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Initialize the figure
fig = go.Figure()

# Add traces by iterating through the chart_data
# The order in JSON determines the drawing layer (bottom to top)
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    series_type = series.get('type', 'line')

    if series_type == 'area':
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(width=0, color=color),
            fill='tozeroy',
            fillcolor=color,
            hoverinfo='skip'
        ))
    else:  # Default to 'line'
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(width=2.5, color=color),
            hoverinfo='skip'
        ))

# Configure layout
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(family="Arial", color='white'),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    # Reverse trace order for legend to match original image (Red, Green, Blue)
    legend_traceorder='reversed',
    margin=dict(l=20, r=20, t=20, b=50),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        title_text=texts.get('y_axis_title')
    )
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.01,
        y=-0.08,  # Position below the plot area
        xanchor='left',
        yanchor='top',
        font=dict(size=10)
    )

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2, width=600, height=480)

print(f"Chart saved to {output_filename}")