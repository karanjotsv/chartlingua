import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for Plotly
y_labels = [item['label'] for item in data]
x_values = [item['value'] for item in data]
color_keys = [item['color_key'] for item in data]

# Create styled tick labels for the y-axis using HTML
styled_y_labels = []
for label, key in zip(y_labels, color_keys):
    color = colors['label_colors'][key]
    # Sanitize label for HTML
    label_safe = label.replace('<', '&lt;').replace('>', '&gt;')
    styled_y_labels.append(f'<span style="color:{color};">{label_safe}</span>')

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_labels,
    orientation='h',
    marker=dict(color=colors['bar_color']),
    hoverinfo='none',
    texttemplate='%{x:,}',
    textposition='none' # Hide default text; we'll use annotations
))

# Add annotations for value labels with specific colors
for i, item in enumerate(data):
    value = item['value']
    color_key = item['color_key']
    color = colors['label_colors'][color_key]
    
    fig.add_annotation(
        x=value,
        y=i,
        text=f"{value:,}",
        showarrow=False,
        xanchor='left',
        xshift=5,
        font=dict(
            family="Arial",
            size=10,
            color=color
        ),
        align='left'
    )

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor=colors['grid_color'],
        zeroline=False
    ),
    yaxis=dict(
        autorange='reversed',  # Ensure the top item in the data is at the top of the chart
        tickmode='array',
        tickvals=list(range(len(y_labels))),
        ticktext=styled_y_labels,
        ticks='',
        showline=False
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor=colors['background_color'],
    paper_bgcolor=colors['background_color'],
    margin=dict(l=300, r=60, t=100, b=80),
    height=700,
    width=1000
)

# Determine output filename from input JSON path
base_name = json_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")