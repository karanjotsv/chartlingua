import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
background_color = chart_data.get('background_color', '#FFFFFF')

# Prepare data for Plotly
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=180 # Starts the first slice at the 9 o'clock position
)])

# Update layout for a professional appearance
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>" if texts.get('title') else None,
        x=0.5,
        xanchor='center',
        font=dict(size=22)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(t=100, b=120, l=40, r=40)
)

# Determine output filename from the input JSON filename
if '.' in json_path:
    output_filename = json_path.rsplit('.', 1)[0] + '.png'
else:
    output_filename = json_path + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")