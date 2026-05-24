import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Determine text position based on value to match the original chart's appearance
# Positive values > 5 are 'inside', others are 'outside'
text_positions = ['inside' if v > 5 else 'outside' for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f"{v:.1f}%" for v in values],
    textposition=text_positions,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts['xaxis_title'],
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False,
        tickfont=dict(size=12),
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts['yaxis_title'],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        range=[-8, 14],
        dtick=2.5,
        ticksuffix='%'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('note', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom'
        ),
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Add a bold zero line
fig.add_hline(y=0, line_width=1.5, line_color="black")

# Define the output filename and save the image
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")