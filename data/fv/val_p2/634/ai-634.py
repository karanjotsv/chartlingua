import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Derive the output PNG filename from the JSON filename
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(family="Arial", size=14),
    sort=False,  # Preserve the order from the JSON file
    direction='counterclockwise' # Plotly's default direction matches the visual analysis
))

# Update layout for title, legend, fonts, and other styling
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,  # Position legend below the chart
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    paper_bgcolor='#E9E7F6',
    plot_bgcolor='#E9E7F6',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=50, r=50, t=100, b=100), # Add margins to prevent clipping
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# To slightly emulate the 3D/raised look, we can add a small pull to each slice
fig.update_traces(pull=[0.03] * len(labels))


# Write the output image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")