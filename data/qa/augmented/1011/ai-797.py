import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
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
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)


# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

x_data = [item['x'] for item in chart_data]
y_data = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_data,
    y=y_data,
    marker_color=colors[0] if colors else None,
    name='' # No legend item
))

# Update layout for a professional appearance
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickvals=x_data,
        tickangle=0,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 300000],
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='solid',
        linecolor='black',
        tickformat='d', # Use 'd' for integer formatting, Plotly handles spacing
        ticksuffix=' ' # Add a space to prevent crowding
    ),
    margin=dict(l=120, r=30, t=30, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Derive the output filename from the input JSON path
output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")