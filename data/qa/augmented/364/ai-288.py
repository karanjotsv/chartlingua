import sys
import os
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
x_values = [item['x'] for item in chart_data['chart_data']]
y_values = [item['y'] for item in chart_data['chart_data']]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=chart_data['colors'][0],
    name=''
))

# Update layout for a professional look and feel
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title=dict(
        text=chart_data['texts']['title'],
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=chart_data['texts']['x_axis_title'],
        type='category',
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=chart_data['texts']['y_axis_title'],
        range=[0, 6000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000],
        ticktext=['0', '1 000', '2 000', '3 000', '4 000', '5 000', '6 000'],
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=chart_data['texts']['source'],
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.20,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color='grey')
        )
    ]
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")