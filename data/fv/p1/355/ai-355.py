import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickangle=-45,
        automargin=True,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 90],
        tickvals=[i for i in range(0, 91, 10)],
        tickformat='.0f',
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=150) # Increased bottom margin for tilted labels
)

# Derive output filename from JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")