import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
x_axis_data = chart_data['x_axis']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data['series']):
    show_in_legend = series.get('name') is not None
    fig.add_trace(go.Bar(
        x=x_axis_data,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        showlegend=show_in_legend
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><span style='font-size:0.8em;color:gray;'>{texts['subtitle']}</span>"

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    title_text=title_text if title_text else None,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1.0,
        xanchor="left",
        x=1.02,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=250, t=50, b=80),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#D3D3D3',
        range=[0, 30],
        tickvals=[0, 5, 10, 15, 20, 25, 30],
        zeroline=True,
        zerolinecolor='black'
    )
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")