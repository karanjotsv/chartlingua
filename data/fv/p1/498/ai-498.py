import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
labels = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0, 0.6]) # Position pie on the left
))

# Create a custom legend using annotations and shapes
legend_x_marker = 0.66
legend_x_text = 0.70
legend_y_start = 0.85
legend_y_step = 0.2

# Add top line for the custom legend
fig.add_shape(
    type="line", xref="paper", yref="paper",
    x0=legend_x_marker - 0.04, y0=legend_y_start + legend_y_step / 2.5,
    x1=0.98, y1=legend_y_start + legend_y_step / 2.5,
    line=dict(color="darkgrey", width=1)
)

for i, (item, color) in enumerate(zip(data, colors)):
    y_pos = legend_y_start - i * legend_y_step
    
    # Add colored marker
    fig.add_shape(
        type="circle", xref="paper", yref="paper",
        x0=legend_x_marker - 0.018, y0=y_pos - 0.018,
        x1=legend_x_marker + 0.018, y1=y_pos + 0.018,
        fillcolor=color, line_color=color
    )
    
    # Add text label
    fig.add_annotation(
        xref="paper", yref="paper",
        x=legend_x_text, y=y_pos,
        text=item['category'],
        showarrow=False,
        xanchor='left', yanchor='middle',
        align='left',
        font=dict(family="Arial", size=18, color="#555555")
    )
    
    # Add line separator
    fig.add_shape(
        type="line", xref="paper", yref="paper",
        x0=legend_x_marker - 0.04, y0=y_pos - legend_y_step / 2.5,
        x1=0.98, y1=y_pos - legend_y_step / 2.5,
        line=dict(color="darkgrey", width=1)
    )

# Add source text annotation
if texts.get('source'):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.3, y=-0.05,
        text=texts['source'],
        showarrow=False,
        xanchor='center', yanchor='top',
        font=dict(family="Arial", size=16, color="#555555")
    )

# Update layout
fig.update_layout(
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=800,
    height=500,
    margin=dict(l=40, r=40, t=40, b=80),
    font=dict(family="Arial")
)

# Define output filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")