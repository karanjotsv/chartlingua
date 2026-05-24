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
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data from the JSON object
chart_data_main = chart_config['chart_data']['main']
chart_data_breakdown = chart_config['chart_data']['breakdown']
texts = chart_config['texts']
colors_main = chart_config['colors']['main']
colors_breakdown = chart_config['colors']['breakdown']

# Create the figure
fig = go.Figure()

# Add the main pie chart (left)
fig.add_trace(go.Pie(
    labels=[d['label'] for d in chart_data_main],
    values=[d['value'] for d in chart_data_main],
    marker_colors=colors_main,
    domain={'x': [0, 0.48], 'y': [0.2, 0.8]},
    pull=[0, 0.2, 0],
    textinfo='none',
    showlegend=False,
    sort=False,
    direction='clockwise',
    rotation=100
))

# Add the breakdown pie chart (right)
fig.add_trace(go.Pie(
    labels=[d['label'] for d in chart_data_breakdown],
    values=[d['value'] for d in chart_data_breakdown],
    marker_colors=colors_breakdown,
    domain={'x': [0.52, 1.0], 'y': [0, 1]},
    textinfo='none',
    showlegend=False,
    sort=False,
    direction='clockwise',
    rotation=90
))

# Add annotations to serve as custom legends
annotations = []

# Main legend (bottom-left)
y_pos_main = 0.25
annotations.append(dict(
    x=0.05, y=y_pos_main, text=texts['legend_title_main'],
    showarrow=False, align='left', xanchor='left', yanchor='top',
    font=dict(family="Arial", size=14)
))
y_pos_main -= 0.05
for i, item in enumerate(chart_data_main):
    annotations.append(dict(
        x=0.05, y=y_pos_main,
        text=f'<span style="color:{colors_main[i]}; font-size:20px;">■</span> {item["label"]} {item["value"]}%',
        showarrow=False, align='left', xanchor='left', yanchor='top',
        font=dict(family="Arial", size=12)
    ))
    y_pos_main -= 0.05

# Breakdown legend (top-right)
y_pos_breakdown = 0.95
annotations.append(dict(
    x=0.73, y=y_pos_breakdown, text=texts['legend_title_breakdown'],
    showarrow=False, align='left', xanchor='left', yanchor='top',
    font=dict(family="Arial", size=14)
))
y_pos_breakdown -= 0.05
for i, item in enumerate(chart_data_breakdown):
    # Format value to remove trailing zeros for small numbers
    value_str = f"{item['value']:.3f}".rstrip('0').rstrip('.')
    annotations.append(dict(
        x=0.73, y=y_pos_breakdown,
        text=f'<span style="color:{colors_breakdown[i]}; font-size:20px;">■</span> {item["label"]}',
        showarrow=False, align='left', xanchor='left', yanchor='top',
        font=dict(family="Arial", size=12)
    ))
    annotations.append(dict(
        x=0.98, y=y_pos_breakdown, text=f"{value_str}%",
        showarrow=False, align='right', xanchor='right', yanchor='top',
        font=dict(family="Arial", size=12)
    ))
    y_pos_breakdown -= 0.045

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.75,
    title_y=0.25,
    title_xanchor='center',
    title_yanchor='top',
    title_font=dict(family="Arial", size=24),
    font_family="Arial",
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    annotations=annotations,
    margin=dict(t=20, b=20, l=20, r=20),
    width=800,
    height=500
)

# Add connector lines
fig.add_shape(type="line", xref="paper", yref="paper",
              x0=0.43, y0=0.68, x1=0.52, y1=0.95,
              line=dict(color="black", width=1))
fig.add_shape(type="line", xref="paper", yref="paper",
              x0=0.42, y0=0.32, x1=0.52, y1=0.05,
              line=dict(color="black", width=1))

# Generate the output image file name from the JSON file name
output_filename = json_file_path.stem + ".png"

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")