import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# Create the figure
fig = go.Figure()

# Add traces from the chart data
for i, series in enumerate(chart_data):
    # Format bar labels with a space as a thousands separator
    bar_texts = [f"{val:,}".replace(",", " ") for val in series['y']]
    
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        # Make the text on bars appear bold as in the original image
        texttemplate='<b>%{text}</b>'
    ))

# Build combined title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Build combined source string
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 40000],
        gridcolor='#E5E5E5',
        zeroline=False,
        # Manually set ticks and labels to match the space separator format
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000],
        ticktext=['0', '5 000', '10 000', '15 000', '20 000', '25 000', '30 000', '35 000', '40 000'],
        tickfont=dict(size=12)
    ),
    # Add margins to prevent clipping of text labels and source
    margin=dict(t=50, b=80, l=80, r=40),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Define the output file name based on the input JSON file name
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")