import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Derive the base filename for the output PNG from the input JSON filename.
base_filename = json_file_path.stem

# Load all data, text, and styling from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config["chart_data"]
texts = chart_config["texts"]
colors = chart_config["colors"]

# Initialize the figure.
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON.
# The order of series in the JSON determines the stacking order.
for i, series in enumerate(chart_data["series"]):
    fig.add_trace(go.Bar(
        x=chart_data["categories"],
        y=series["data"],
        name=series["name"],
        marker_color=colors[i],
        text=series["data"],
        textposition='inside',
        texttemplate='%{y}',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=12)
    ))

# Configure the chart layout.
fig.update_layout(
    barmode='stack',
    title_text=texts.get("title"),
    yaxis_title_text=texts.get("y_axis_title"),
    xaxis_title_text=texts.get("x_axis_title"),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2, # Position legend below the x-axis
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 300], # Set a fixed range to match the original chart
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100) # Adjust margins for titles and legend
)

# Add source text as an annotation at the bottom right.
if texts.get("source"):
    fig.add_annotation(
        text=texts["source"],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.2, # Position below the legend
        font=dict(family="Arial", size=11, color="#666666"),
        xanchor='right',
        yanchor='top'
    )

# Generate and save the chart as a high-resolution PNG image.
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")