import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Derive the base filename for the output image
# e.g., "path/to/my_chart.json" -> "my_chart"
base_filename = json_file_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_image_path = f"{base_filename}.png"

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly Pie chart
labels = [f"{item['label']} ({item['value']}%)" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for styling, title, font, and margins
fig.update_layout(
    title_text=f"<b>{texts.get('title', '')}</b>",
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        traceorder='normal',
        x=1.05,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(t=100, b=50, l=50, r=250),
    showlegend=True
)

# Generate and save the image
try:
    fig.write_image(output_image_path, scale=2, width=900, height=600)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)