import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
categories = [d['category'] for d in chart_info['chart_data']]
values = [d['value'] for d in chart_info['chart_data']]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=chart_info['colors'][0],
    name='' # Hide legend entry for a single series
))

# Update layout
fig.update_layout(
    template="plotly_white",
    font_family="Arial",
    title_text=chart_info['texts'].get('title'),
    yaxis_title=chart_info['texts'].get('y_axis_title'),
    xaxis_title=chart_info['texts'].get('x_axis_title'),
    yaxis=dict(
        range=[0, 5000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000],
        gridcolor='lightgray'
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=chart_info['texts'].get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

# Generate output filename from the input JSON path
if '.' in json_file_path:
    base_name = json_file_path.rsplit('.', 1)[0]
else:
    base_name = json_file_path

output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")