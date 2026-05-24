import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON object.
data_points = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data series for Plotly.
categories = [item['category'] for item in data_points]
values = [item['value'] for item in data_points]

# Create a new figure object.
fig = go.Figure()

# Add a bar trace for the data series.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Apply HTML styling to color the info icons in the note and source text.
note_text = texts.get('note', '').replace('ⓘ', '<span style="color:#3498DB;">ⓘ</span>')
source_text = texts.get('source', '').replace('ⓘ', '<span style="color:#3498DB;">ⓘ</span>')

# Configure the chart layout, including fonts, axes, margins, and annotations.
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2],
        tickmode='array',
        tickvals=[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.3,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        ),
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Derive the output filename from the input JSON file's base name.
output_filename_base = Path(json_file_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the generated chart to a high-resolution PNG file.
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")