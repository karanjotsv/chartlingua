import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data and text from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# Prepare data for Plotly
x_values = [d['year'] for d in chart_data]
y_values = [d['price'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    marker_line_width=0,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout for a professional look, matching the source image
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        tickvals=x_values,
        ticktext=[str(year) for year in x_values]
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 1000],
        tickvals=[0, 200, 400, 600, 800, 1000],
        ticktext=['0', '200', '400', '600', '800', '1 000'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    margin=dict(l=90, r=40, t=40, b=80),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(
                size=12
            )
        )
    ]
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")