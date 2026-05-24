import sys
import json
import os
import plotly.graph_objects as go

# Check for required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Initialize the figure
fig = go.Figure()

# Add traces for each data series from the JSON
for i, series in enumerate(chart_config["chart_data"]):
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        name=series["name"],
        mode='lines+markers+text',
        line=dict(color=chart_config["colors"][i], width=2.5),
        marker=dict(color=chart_config["colors"][i], size=8),
        text=[f'{val:.1f}' for val in series["y"]],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='skip'
    ))

# Build title and source strings from JSON
title_text = chart_config["texts"]["title"] if chart_config["texts"]["title"] else ""
if chart_config["texts"]["subtitle"]:
    title_text += f'<br><sub>{chart_config["texts"]["subtitle"]}</sub>'

source_text = chart_config["texts"]["source"] if chart_config["texts"]["source"] else ""

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=chart_config["texts"]["x_axis_title"],
        tickmode='array',
        tickvals=chart_config["chart_data"][0]["x"],
        ticktext=[str(x) for x in chart_config["chart_data"][0]["x"]],
        showgrid=True,
        gridcolor='#F0F0F0',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=chart_config["texts"]["y_axis_title"],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[33, 39.5]
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    margin=dict(l=70, r=40, t=60, b=120),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.3,
            xanchor='left', yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

# Derive output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)