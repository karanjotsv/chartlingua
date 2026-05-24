import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Create a figure with two subplots
fig = make_subplots(
    rows=1, cols=2,
    shared_yaxes=True,
    horizontal_spacing=0.05
)

seen_legends = set()

# Iterate over the subplot data from the JSON
for i, subplot in enumerate(chart_data["subplots"]):
    col_index = i + 1
    texts = subplot["texts"]
    colors = subplot["colors"]

    # Iterate over each data series for the current subplot
    for j, series in enumerate(subplot["chart_data"]):
        # Add trace only if the name has not been seen before for legend purposes
        show_legend = series["name"] not in seen_legends
        fig.add_trace(
            go.Scatter(
                x=series["x"],
                y=series["y"],
                name=series["name"],
                mode='lines',
                line=dict(
                    color=colors[j],
                    width=2,
                    dash=series["dash"]
                ),
                showlegend=show_legend,
                legendgroup=series["name"]
            ),
            row=1,
            col=col_index
        )
        if show_legend:
            seen_legends.add(series["name"])

    # Update axes for the current subplot
    fig.update_xaxes(
        title_text=texts["x_axis_title"],
        row=1,
        col=col_index,
        range=[0, 1.8],
        tickmode='linear',
        dtick=0.2,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        ticks='outside',
        gridcolor='#E5E5E5'
    )

# Update Y axes (applies to both since they are shared)
fig.update_yaxes(
    title_text=chart_data["subplots"][0]["texts"]["y_axis_title"],
    range=[-80, 20],
    tickmode='linear',
    dtick=10,
    showline=True,
    linewidth=1.5,
    linecolor='black',
    mirror=True,
    ticks='outside',
    gridcolor='#E5E5E5'
)

# Update overall layout
fig.update_layout(
    width=1000,
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=70, r=30, b=100, t=30),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='black',
        borderwidth=0
    )
)


# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")