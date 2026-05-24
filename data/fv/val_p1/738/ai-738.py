import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=[f'{v:.1f}%' for v in values],
    textposition='auto',
    insidetextanchor='end',
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        showline=False,
        zeroline=False,
        range=[0, 30],
        dtick=5,
        ticksuffix='%'
    ),
    margin=dict(l=60, r=40, t=80, b=80),
    barmode='group'
)
# Adjust text font size and position
fig.update_traces(textfont_size=12, textangle=0)


# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)