import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
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
fig.add_trace(
    go.Bar(
        x=x_values,
        y=y_values,
        marker_color=chart_data['colors'][0],
        text=[f"{y:.2f}" for y in y_values],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    )
)

# Update layout for a clean and accurate look
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=chart_data['texts']['title'] or '',
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=chart_data['texts']['x_axis_title'] or '',
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=chart_data['texts']['y_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        showline=False,
        zeroline=False,
        range=[0, 35],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35],
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=[
        dict(
            text=chart_data['texts']['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10)
        )
    ]
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")