import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive base filename for output
filename_base = os.path.splitext(os.path.basename(json_path))[0]

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
legend_labels = chart_data['legend_labels']

# Prepare data for main and breakout pie charts
main_labels = [d['label'] for d in data['main']]
main_values = [d['value'] for d in data['main']]
breakout_labels = [d['label'] for d in data['breakout']]
breakout_values = [d['value'] for d in data['breakout']]

# Create figure
fig = go.Figure()

# Add the main pie chart trace
fig.add_trace(go.Pie(
    labels=main_labels,
    values=main_values,
    marker_colors=colors['main'],
    domain={'x': [0, 0.48], 'y': [0.05, 0.95]},
    name='Countries of Origin',
    textinfo='percent',
    textfont=dict(color='white', size=14),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=False
))

# Add the breakout pie chart trace
fig.add_trace(go.Pie(
    labels=breakout_labels,
    values=breakout_values,
    marker_colors=colors['breakout'],
    domain={'x': [0.52, 1.0], 'y': [0.2, 0.8]},
    name='Other Countries',
    textinfo='percent',
    textfont=dict(color='white', size=14),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    showlegend=False
))

# Create a comprehensive color map for the custom legend
color_map = {}
for item, color in zip(data['main'], colors['main']):
    if item['label'] != 'Other':
        color_map[item['label']] = color
for item, color in zip(data['breakout'], colors['breakout']):
    color_map[item['label']] = color
color_map['New Zealand'] = colors['new_zealand']

# Build the ordered list of colors for the legend
ordered_legend_colors = [color_map.get(label, '#000000') for label in legend_labels]

# Add invisible scatter traces to create the custom legend
for label, color in zip(legend_labels, ordered_legend_colors):
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(symbol='square', color=color, size=12),
        name=label,
        showlegend=True
    ))

# Add connecting lines between the two pies
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0.46, y0=0.6, x1=0.52, y1=0.8,
    line=dict(color="grey", width=1)
)
fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0.46, y0=0.4, x1=0.52, y1=0.2,
    line=dict(color="grey", width=1)
)

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_y=0.95,
    font=dict(family="Arial", size=14),
    margin=dict(t=80, b=120, l=20, r=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font=dict(size=12)
    )
)

# Output image file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2, width=1200, height=700)

print(f"Chart saved to {output_filename}")