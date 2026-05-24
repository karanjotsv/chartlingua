import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data structures for Plotly
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]
display_texts = [item.get('display_text', '') for item in chart_data]

# Define text positions based on the original chart's layout
text_positions = ['inside', 'outside', 'outside', 'outside', 'outside', 'inside']

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=display_texts,
    textinfo='text',
    textposition=text_positions,
    insidetextfont=dict(color='white', size=16),
    outsidetextfont=dict(color='black', size=14),
    marker=dict(
        colors=colors,
        line=dict(color='black', width=2)
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=90
)])

# Update the figure's layout for a clean and accurate presentation
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    title_font=dict(size=24, family="Arial"),
    font=dict(family="Arial"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=40, l=40, r=40)
)

# Derive the output filename from the input JSON filename
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure to a high-resolution PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)