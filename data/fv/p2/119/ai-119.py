import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read the chart data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for the Plotly pie chart
display_labels = [item['display_label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=display_labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    textposition='outside',
    textinfo='label',  # Use the 'labels' list for the text on the chart
    hoverinfo='label+percent+value'
)])

# Combine the title and subtitle using HTML for formatting
full_title = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    full_title += f"<br>{texts['subtitle']}"

# Configure the chart layout
fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(t=120, b=80, l=80, r=80),  # Adjust margins to prevent clipping
    paper_bgcolor='white'
)

# Determine the output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the generated chart as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)