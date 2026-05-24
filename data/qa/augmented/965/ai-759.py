import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Create a figure object
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_json['chart_data']):
    # Create string versions of values to preserve original formatting
    text_labels = [str(v) for v in series['values']]

    fig.add_trace(go.Bar(
        y=series['categories'],
        x=series['values'],
        orientation='h',
        marker=dict(color=chart_json['colors'][i]),
        text=text_labels,
        textposition='outside',
        cliponaxis=False,
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=180, r=40, t=40, b=80),
    xaxis=dict(
        title=chart_json['texts']['x_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        separatethousands=True,
        tickformat=',.0f'
    ),
    yaxis=dict(
        title=chart_json['texts']['y_axis_title'],
        showgrid=False
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            text=chart_json['texts']['source'],
            showarrow=False,
            font=dict(size=10)
        )
    ]
)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")