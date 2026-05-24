import sys
import json
import os
import plotly.graph_objects as go

# Ensure a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for the Plotly pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#404040', width=2)),
    texttemplate='%{value}%',
    textfont=dict(color='white', size=12, family='Arial'),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the input data
    direction='clockwise',
    rotation=100
)])

# Update the figure's layout and styling
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family='Arial', size=18, color='white')
    ),
    paper_bgcolor='#404040',
    plot_bgcolor='#404040',
    font=dict(family='Arial', color='white'),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5,
        font=dict(family='Arial', size=12, color='white')
    ),
    margin=dict(l=40, r=40, t=80, b=80),
    showlegend=True
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a specified scale for high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")