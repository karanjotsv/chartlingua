import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python your_script_name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data elements from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize a Plotly Figure
fig = go.Figure()

# Add a separate Bar trace for each data point to control legend and color individually
for i, entry in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=entry['label'],
        x=[entry['label']],
        y=[entry['value']],
        marker_color=colors[i],
        text=[str(entry['value'])],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=12),
        width=0.7
    ))

# Configure the chart layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title_text=texts.get('title'),
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    plot_bgcolor='white',
    showlegend=True,
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        categoryorder='array',
        categoryarray=[d['label'] for d in chart_data]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-150, 550],
        dtick=100
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=70, r=30, t=90, b=90)
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")