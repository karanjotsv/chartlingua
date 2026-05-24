import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for Plotly; reverse order to match visual top-to-bottom
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='none' # We will use annotations for more control
))

# Add data labels as annotations next to each bar
for i, (value, category) in enumerate(zip(values, categories)):
    fig.add_annotation(
        x=value,
        y=category,
        text=str(value),
        showarrow=False,
        xanchor='left',
        xshift=5,
        yanchor='middle',
        font=dict(
            family="Arial",
            size=12,
            color="black"
        )
    )

# Update layout for a clean and accurate look
fig.update_layout(
    font=dict(family="Arial", size=12),
    title_text=texts.get('title'),
    xaxis_title_text=texts.get('x_axis_title'),
    yaxis_title_text=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=300, r=40, t=50, b=80),
    xaxis=dict(
        range=[0, max(values) * 1.2], # Ensure space for labels
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    )
)

# Add source text as an annotation
fig.add_annotation(
    text=texts.get('source'),
    xref="paper", yref="paper",
    x=0.98, y=-0.1,
    showarrow=False,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(size=12)
)

# Determine output filename from input JSON path
base_filename = pathlib.Path(json_file_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")