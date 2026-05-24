import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path_str = sys.argv[1]
json_path = pathlib.Path(json_file_path_str)

# Check if the file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False  # Prevents text on top of bars from being clipped
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.2,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        range=[0, 70],
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12),
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    annotations=[
        dict(
            text=f"ⓘ {texts.get('additional_info_link', '')}",
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            font=dict(color="#007bff")
        ),
        dict(
            text=texts.get('source_copyright', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            font=dict(color="#6c757d")
        ),
        dict(
            text=f"{texts.get('source_link', '')} ⓘ",
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            font=dict(color="#007bff")
        )
    ]
)

# Generate output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")