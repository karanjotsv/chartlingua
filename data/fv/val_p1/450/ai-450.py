import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for the correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the specified file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data and texts for convenience
chart_data = data['chart_data']
legend_data = data['legend_data']
texts = data['texts']
color_map = dict(zip(legend_data['labels'], legend_data['colors']))

# Prepare subplot titles, placing them according to the 2x2 grid layout
subplot_titles = [
    chart_data[0]['year'],
    chart_data[1]['year'],
    "",  # Placeholder for the legend area
    chart_data[2]['year']
]

# Initialize a figure with a 2x2 grid of subplots for the pie charts
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}],
           [{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=subplot_titles
)

# Define the positions for the three pie charts in the 2x2 grid
positions = [(1, 1), (1, 2), (2, 2)]

# Iterate through the chart data and add a pie trace for each year
for i, chart_info in enumerate(chart_data):
    row, col = positions[i]
    labels = chart_info['labels']
    values = chart_info['values']
    slice_colors = [color_map.get(label) for label in labels]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(
                colors=slice_colors,
                line=dict(color='#000000', width=2)
            ),
            texttemplate='<b>%{percent:.0%}</b>',
            textfont=dict(color='white', size=18),
            hoverinfo='label+percent',
            sort=False,
            showlegend=False,
            direction='clockwise'
        ),
        row=row,
        col=col
    )

# --- Create a custom legend in the empty subplot area (bottom-left) ---
legend_x = 0.18
legend_y_start = 0.38
legend_y_step = 0.09
legend_swatch_size = 0.04
legend_text_offset = 0.06

# Add legend title
fig.add_annotation(
    text=f"<b>{texts['legend_title']}</b>",
    x=legend_x, y=legend_y_start + 0.06,
    xref="paper", yref="paper",
    showarrow=False,
    xanchor='left',
    font=dict(size=16, family="Arial")
)

# Add legend items (color swatch + text label)
for i, label in enumerate(legend_data['labels']):
    y_pos = legend_y_start - (i * legend_y_step)
    
    # Add color swatch (a filled rectangle)
    fig.add_shape(
        type="rect",
        x0=legend_x, y0=y_pos,
        x1=legend_x + legend_swatch_size, y1=y_pos + legend_swatch_size,
        xref="paper", yref="paper",
        fillcolor=color_map[label],
        line_width=1,
        line_color='black'
    )
    # Add text label
    fig.add_annotation(
        text=label,
        x=legend_x + legend_text_offset, y=y_pos + (legend_swatch_size / 2),
        xref="paper", yref="paper",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(size=15, family="Arial")
    )
# Add a border around the custom legend
fig.add_shape(
    type="rect",
    x0=legend_x - 0.03, y0=0.05,
    x1=legend_x + 0.25, y1=legend_y_start + 0.12,
    xref="paper", yref="paper",
    line_color="Black",
    line_width=1
)

# --- Final layout and styling adjustments ---
fig.update_layout(
    title_text=f"<b>{texts['title']}</b>",
    title_x=0.5,
    title_font=dict(size=24, family="Arial"),
    margin=dict(t=100, b=40, l=40, r=40),
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=800,
    height=800
)

# Update font size and family for subplot titles
for annotation in fig.layout.annotations:
    if annotation.text in subplot_titles:
        annotation.font.size = 20
        annotation.font.family = "Arial"

# --- Output the chart to a PNG file ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")