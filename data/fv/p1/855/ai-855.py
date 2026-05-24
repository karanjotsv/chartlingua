import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure object
fig = go.Figure()

# Add the first pie chart trace
fig.add_trace(go.Pie(
    labels=data['pie1']['labels'],
    values=data['pie1']['values'],
    domain={'x': [0, 0.48], 'y': [0.1, 0.9]},
    marker={
        'colors': colors['pie1_slices'],
        'line': {'color': '#000000', 'width': 2}
    },
    texttemplate='%{value}%',
    textposition='inside',
    insidetextorientation='radial',
    insidetextfont={
        'family': 'Arial',
        'size': 16,
        'color': 'white'
    },
    sort=False,
    direction='clockwise'
))

# Update text color for the first pie chart based on JSON data
fig.data[0].insidetextfont.color = colors['pie1_text']

# Add the second pie chart trace
fig.add_trace(go.Pie(
    labels=data['pie2']['labels'],
    values=data['pie2']['values'],
    domain={'x': [0.52, 1], 'y': [0.1, 0.9]},
    marker={
        'colors': colors['pie2_slices'],
        'line': {'color': '#000000', 'width': 2}
    },
    texttemplate='%{value}%',
    textposition='inside',
    insidetextorientation='radial',
    insidetextfont={
        'family': 'Arial',
        'size': 16,
        'color': 'black'
    },
    sort=False,
    direction='clockwise'
))

# Update text color for the second pie chart based on JSON data
fig.data[1].insidetextfont.color = colors['pie2_text']


# Update layout for a clean and accurate representation
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font={'size': 20},
    showlegend=True,
    legend={
        'traceorder': 'normal',
        'font': {'family': 'Arial', 'size': 12, 'color': 'white'},
        'bgcolor': 'rgba(0,0,0,0)',
        'bordercolor': 'rgba(0,0,0,0)'
    },
    plot_bgcolor='black',
    paper_bgcolor='black',
    font={'family': 'Arial', 'color': 'white'},
    margin={'t': 80, 'b': 40, 'l': 40, 'r': 40}
)

# Define the output image path from the input JSON filename
output_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved to '{output_path}'")