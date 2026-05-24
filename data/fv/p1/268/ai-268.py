import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the base filename for the output image from the JSON file path
# e.g., "path/to/my_chart.json" -> "my_chart"
base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]

# Load data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the Plotly pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{value}%',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=24,
        color='black'
    ),
    pull=[0.05, 0.05, 0.05],  # Explode slices to mimic the original chart's 3D separation
    sort=False,  # Preserve the original data order
    direction='clockwise',
    hole=0 # Ensure it's a pie chart, not a donut
))

# Update layout to match the original chart's aesthetics
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        font=dict(family="Arial", size=24, color='black'),
        x=0.5,
        xanchor='center'
    ),
    showlegend=True,
    legend=dict(
        font=dict(family="Arial", size=18, color='black'),
        x=1,
        y=1,
        xanchor='right',
        yanchor='top'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=18, color='black'),
    margin=dict(l=40, r=40, t=100, b=40) # Adjust margins to prevent clipping
)

# Generate the output image file
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")