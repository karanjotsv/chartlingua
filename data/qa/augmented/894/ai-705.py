import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Configure layout
annotations = []
if texts.get("note"):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts["note"],
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

if texts.get("source"):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts["source"],
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50],
        gridcolor='#E0E0E0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations
)

# Generate output filename from the input JSON filename
output_filename = json_path.with_suffix('.png').name

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")