import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
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
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    hoverinfo='none',
    cliponaxis=False # Allows text to render outside the plot area
))

# Update trace appearance
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

# Configure the layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        tickmode='array',
        tickvals=x_values,
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 1050],
        tickvals=[0, 200, 400, 600, 800, 1000],
        ticktext=['0', '200', '400', '600', '800', '1 000'],
        showgrid=True,
        gridcolor='lightgrey',
        linecolor='black',
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts.get("source"),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Generate the output filename from the input JSON path
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")