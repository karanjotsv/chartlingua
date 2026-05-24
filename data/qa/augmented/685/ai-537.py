import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart_data
for i, series in enumerate(chart_data):
    # Use the color for the current series, or a default if not specified
    color = colors[i] if i < len(colors) else None
    
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines+markers+text',
        name=series.get("name", ""),
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=7),
        text=[f'{y:.2f}' if y != 1 else '1' for y in series.get("y", [])],
        textposition='top center',
        textfont=dict(
            family="Arial, sans-serif",
            size=12,
            color='black'
        )
    ))

# Combine title and subtitle using HTML line breaks
title_text = texts.get("title", "")
subtitle_text = texts.get("subtitle", "")
if title_text and subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
elif title_text:
    title_text = f"<b>{title_text}</b>"

# Combine source and note for the footer annotation
source_text = texts.get("source", "")
note_text = texts.get("note", "")
footer_text = ""
if source_text:
    footer_text += source_text
if note_text:
    # Adding a small visual separation if both exist
    footer_text += "<br>" + note_text if source_text else note_text

# Update layout
fig.update_layout(
    font=dict(family="Arial, sans-serif", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    xaxis=dict(
        showline=True,
        showgrid=False,
        linecolor='lightgray',
        tickmode='array',
        tickvals=chart_data[0]['x'] if chart_data else None,
        ticktext=[str(year) for year in chart_data[0]['x']] if chart_data else None
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=False,
        range=[0.85, 1.1],
        tickmode='array',
        tickvals=[0.85, 0.9, 0.95, 1, 1.05, 1.1]
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=60, b=100) # Adjust margins for titles and footer
)

# Add footer annotation for source and note
if footer_text:
    fig.add_annotation(
        text=footer_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=11, color="#555555")
    )
    
# Define output filename based on the input JSON file's base name
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image with a higher scale for better quality
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")