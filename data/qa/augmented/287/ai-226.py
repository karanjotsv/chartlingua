import sys
import os
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
    
# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
categories = [item['category'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
texts_info = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    texttemplate='%{text}',
    cliponaxis=False 
))

# Update layout
fig.update_layout(
    font_family="Arial",
    paper_bgcolor='#F8F9FA',
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts_info['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts_info['y_axis_title'],
        title_standoff=15,
        range=[0, 2500],
        dtick=500,
        gridcolor='#EAEAEA',
        tickformat=' ',
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts_info['note'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#555555')
        ),
        dict(
            text=texts_info['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color='#555555')
        )
    ]
)

# Set text font properties for the bar labels
fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

# Derive output filename from JSON path
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")