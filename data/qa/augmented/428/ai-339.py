import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors['bar_color'][0],
    cliponaxis=False  # Prevents text labels from being clipped
))

# Update layout for a professional look
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    title_text=texts['title'] if texts.get('title') else None,
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 500],
        tickmode='linear',
        dtick=100,
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#F0F0F0',
        linecolor='black',
        ticks='outside'
    ),
    margin=dict(l=90, r=40, t=50, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#6c757d')
        )
    ]
)

# Update trace properties
fig.update_traces(textfont_size=12)

# Determine output filename and save the image
base_filename, _ = os.path.splitext(os.path.basename(json_file_path))
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")