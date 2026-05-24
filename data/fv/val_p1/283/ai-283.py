import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the first argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the provided path is a valid file
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the chart data from the JSON file, ensuring UTF-8 encoding
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare labels and values for the pie chart trace
# The legend text is formatted as "LABEL (VALUE%)" to match the original image
labels = [f"{item['label']} ({item['value']}%)" for item in data]
values = [item['value'] for item in data]

# Initialize a Figure object
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    sort=False,  # Preserve the original data order from the JSON file
    direction='clockwise',
    textinfo='none',  # Do not display text on the pie slices
    hoverinfo='label+percent'
))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=f"<b><u>{texts['title']}</u></b>",
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=28, color="#1f4962")
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=120, b=120),  # Adjust margins to prevent clipping
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)'
)

# Determine the output image filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure to a PNG image file with a higher resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")