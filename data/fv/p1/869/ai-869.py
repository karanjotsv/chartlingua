import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly, preserving the order from the JSON
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(family="Arial", size=14, color="black"),
    sort=False,
    direction='clockwise',
    rotation=162,
    textposition='outside'
)])

# Update the layout for titles, legend, fonts, and margins
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial",
        color="black"
    ),
    margin=dict(l=40, r=40, t=100, b=100),
    paper_bgcolor='#F0F0FF',
    plot_bgcolor='#F0F0FF'
)

# Determine the output filename from the input JSON filename
output_filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")