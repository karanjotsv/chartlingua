import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data_list = config['chart_data']
texts = config['texts']

# Create a figure with two subplots for the pie charts
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]]
)

# Iterate through the chart data list to create a pie chart for each entry
for i, chart_data in enumerate(chart_data_list):
    fig.add_trace(go.Pie(
        labels=chart_data['labels'],
        values=chart_data['values'],
        marker=dict(
            colors=chart_data['colors'],
            line=dict(color='#000000', width=1)
        ),
        texttemplate='%{label}<br>%{value}%',
        textposition='auto',
        hoverinfo='label+percent',
        insidetextorientation='horizontal',
        sort=False,
        name=''  # Hides trace name on hover
    ), row=1, col=i + 1)

# Update the figure layout with titles, fonts, and other styling
fig.update_layout(
    annotations=[
        dict(
            text=texts['title_1'],
            x=0.22, y=1.08,
            font=dict(family="Arial", size=16, color="black"),
            showarrow=False,
            xanchor='center'
        ),
        dict(
            text=texts['title_2'],
            x=0.78, y=1.08,
            font=dict(family="Arial", size=16, color="black"),
            showarrow=False,
            xanchor='center'
        )
    ],
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(t=80, b=20, l=20, r=20),
    paper_bgcolor='white'
)

# Determine the output filename from the input JSON path
# e.g., 'path/to/chart.json' becomes 'chart.png'
base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")