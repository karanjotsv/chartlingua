import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly (Plotly plots from bottom to top, so reverse the lists)
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors['bar_color'][0],
        line=dict(color=colors['bar_border_color'], width=1.5)
    ),
    text=values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        color=colors['bar_label_color'],
        size=14
    ),
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='Arial',
            size=20,
            color=colors['text_color'],
        )
    ),
    font=dict(
        family='Arial',
        color=colors['text_color']
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        title_text=texts['x_axis_title'],
        range=[0, max(values) * 1.05] # Add padding to the right
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        title_text=texts['y_axis_title'],
        tickfont=dict(
            size=16
        )
    ),
    plot_bgcolor=colors['background_color'],
    paper_bgcolor=colors['background_color'],
    showlegend=False,
    margin=dict(l=150, r=40, t=80, b=40)
)

# Determine output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")