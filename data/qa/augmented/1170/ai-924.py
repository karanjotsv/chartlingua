import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else None,
        text=values,
        textposition='outside',
        texttemplate='%{text}',
        hoverinfo='none',
        cliponaxis=False 
    )
)

# Update layout to match the original image
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        linecolor='lightgrey',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 120],
        dtick=20,
        showgrid=True,
        gridcolor='#DCDCDC',
        linecolor='lightgrey',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    bargap=0.4,
    showlegend=False,
    margin=dict(l=80, r=40, b=100, t=40),
    annotations=[]
)

# Add source annotation if present
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.18,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color="#7f7f7f")
    )

# Update text font on bars
fig.update_traces(textfont=dict(size=12, color='black'))

# Generate and save the output image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)