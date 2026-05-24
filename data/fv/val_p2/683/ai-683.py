import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Create the figure object
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data["chart_data"]):
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        name=series["name"],
        mode='lines',
        line=dict(color=chart_data["colors"][i], width=3)
    ))

# Build title string
title_text = f'<b>{chart_data["texts"]["title"]}</b><br>{chart_data["texts"]["subtitle"]}'

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=16)
    ),
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=chart_data["texts"]["y_axis_title"],
        range=[-45, 0],
        dtick=5,
        gridcolor='#FFFFFF',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='#FFFFFF',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=1,
        y=0.8,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=100, b=40)
)

# Add annotations for x-axis categories
annotations = []
if "x_axis_annotations" in chart_data["texts"]:
    for x_val in chart_data["texts"]["x_axis_annotations"]:
        annotations.append(
            dict(
                x=x_val,
                y=0,
                yref="y",
                xref="x",
                text=x_val,
                showarrow=False,
                yshift=15,
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                )
            )
        )
fig.update_layout(annotations=annotations)


# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")