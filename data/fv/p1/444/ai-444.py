import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the JSON structure
texts = chart_data['texts']
data = chart_data['chart_data']
colors = chart_data['colors']
labels = data['labels']
male_values = data['male_values']
female_values = data['female_values']

# Create subplots for the two pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add the Male Occupation pie chart
fig.add_trace(go.Pie(
    labels=labels,
    values=male_values,
    name="Male",
    marker_colors=colors,
    textinfo='value',
    textposition='auto',
    sort=False,
    hoverinfo='label+percent+value',
    domain=dict(x=[0, 0.5])
), 1, 1)

# Add the Female Occupation pie chart
fig.add_trace(go.Pie(
    labels=labels,
    values=female_values,
    name="Female",
    marker_colors=colors,
    textinfo='value',
    textposition='auto',
    sort=False,
    hoverinfo='label+percent+value',
    domain=dict(x=[0.5, 1.0])
), 1, 2)

# Update layout for titles, legend, and general appearance
fig.update_layout(
    annotations=[
        dict(text=texts['title_left'], x=0.19, y=1.08, font_size=18, showarrow=False),
        dict(text=texts['title_right'], x=0.81, y=1.08, font_size=18, showarrow=False)
    ],
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=80, b=80, l=20, r=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Update traces for consistent styling
fig.update_traces(
    textfont_size=12,
    insidetextorientation='radial'
)

# Determine the output image filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")