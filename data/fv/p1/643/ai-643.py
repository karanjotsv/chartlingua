import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the configuration
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
series_colors = colors['series']
background_color = colors['background']

# Create the figure object
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=series_colors,
    textinfo='percent',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent'
))

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_font_size=24,
    font_family="Arial",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor=background_color,
    paper_bgcolor=background_color,
    margin=dict(t=100, b=100, l=40, r=40)
)

# Derive the output filename from the input JSON file path
# This handles both forward and backward slashes in the path
base_name = json_path.rsplit('.', 1)[0]
if '/' in base_name:
    base_name = base_name.rsplit('/', 1)[1]
if '\\' in base_name:
    base_name = base_name.rsplit('\\', 1)[1]

output_image_path = f"{base_name}.png"

# Write the chart to a PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")