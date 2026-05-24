import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data and configuration from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and texts
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
# Format text labels for display on bars with space as thousands separator
formatted_text_values = [f"{v:,}".replace(",", " ") for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=formatted_text_values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False  # Prevents text labels from being clipped at the top
))

# Update layout for a clean, professional look
fig.update_layout(
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        range=[0, 12000],
        tickmode='linear',
        tick0=0,
        dtick=2000,
        tickformat=" " # Use space as thousands separator
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(
                size=12,
                color='gray'
            )
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_color='black')

# Generate the output filename from the input JSON path
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")