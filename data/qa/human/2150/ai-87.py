import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series = data['series']

# Initialize the figure
fig = go.Figure()

# Iterate through the series data to add a bar trace for each segment
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        name=s['name'],
        x=categories,
        y=s['data'],
        marker_color=colors[i],
        # Format text to match original (space as thousand separator)
        text=[f'{val:,}'.replace(',', ' ') for val in s['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=12, family='Arial', weight='bold')
    ))

# Configure the layout of the chart
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=40, t=40, b=150),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 40000],
        tickvals=[0, 10000, 20000, 30000, 40000],
        ticktext=['0', '10 000', '20 000', '30 000', '40 000'],
        gridcolor='#E5E5E5',
        zeroline=False
    )
)

# Add the source text as an annotation
fig.add_annotation(
    text=texts['source'],
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.98,
    y=-0.45,
    xanchor='right',
    yanchor='bottom',
    font=dict(size=12)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")