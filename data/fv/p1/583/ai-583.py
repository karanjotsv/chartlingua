import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_filepath = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_filepath):
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

# Derive output filename from input filename
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Load data from JSON file
with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=series['y'],
        x=series['x'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='darkgray', width=0.5)
        )
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    xaxis=dict(
        autorange='reversed',
        range=[40, 0],
        tickvals=[0, 10, 20, 30, 40],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        tickfont=dict(color='#006400', size=14)
    ),
    legend=dict(
        x=0.01,
        y=1.0,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=14)
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    margin=dict(l=250, r=20, t=100, b=80),
    height=500,
    width=800
)

# Set axis lines to be visible to create the plot border
fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

# Use an annotation for the custom-placed x-axis title
if texts.get('x_axis_title'):
    fig.add_annotation(
        text=texts['x_axis_title'],
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        showarrow=False,
        align='left',
        font=dict(size=18)
    )

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")