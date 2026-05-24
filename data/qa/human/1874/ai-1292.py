import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for plotting
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the main line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=8),
    showlegend=False
))

# Add data labels as annotations for precise placement
for point in chart_data:
    fig.add_annotation(
        x=point['x'],
        y=point['y'],
        text=str(point['y']),
        showarrow=False,
        font=dict(family="Arial", size=12, color='black'),
        yshift=15 # Shift text above the marker
    )

# Configure layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        linecolor='black',
        tickangle=-30
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[1200, 1400],
        tickvals=[1200, 1225, 1250, 1275, 1300, 1325, 1350, 1375, 1400],
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False
    )
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color="#555555")
    )


# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")