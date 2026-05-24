import sys
import json
import os
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Extract data and texts for plotting
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=[f"{v}%" for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False # Allows text to render outside the plot area
))

# Update layout to match the original chart's appearance
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.25], # Provide enough space for labels
        tickvals=[0, 5, 10, 15, 20, 25, 30]
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(t=30, r=30, b=80, l=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")