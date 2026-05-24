import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Format text labels for bars with space as thousand separator
bar_text_labels = ["{:,}".format(y).replace(",", " ") for y in y_values]

# Create figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=bar_text_labels,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

# Prepare y-axis tick labels
y_tickvals = list(range(0, 25000, 2500))
y_ticktext = ["{:,}".format(v).replace(",", " ") for v in y_tickvals]

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'] if texts.get('title') else '',
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        range=[0, 22500],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickmode='array',
        tickvals=y_tickvals,
        ticktext=y_ticktext
    ),
    annotations=[
        dict(
            x=1,
            y=-0.18,
            showarrow=False,
            text=texts['source'],
            xref="paper",
            yref="paper",
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")