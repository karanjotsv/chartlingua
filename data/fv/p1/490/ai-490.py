import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for plotting
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
    textfont=dict(family="Arial", size=12, color='black'),
    marker=dict(
        color=colors[0],
        line=dict(
            color='#333333',
            width=0.5
        )
    ),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.05,
        y=0.92,
        xanchor='left',
        yanchor='bottom'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        range=[0, 3.5],
        dtick=0.5,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=False,
        zeroline=False,
        side='right',
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=50, t=100, b=80),
    shapes=[
        dict(
            type='line',
            xref='paper', yref='paper',
            x0=0.03, y0=0.98,
            x1=0.20, y1=0.98,
            line=dict(color='black', width=3)
        )
    ],
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.15,
            xanchor='center',
            yanchor='top',
            font=dict(family="Arial", size=10, color='#555555')
        )
    ]
)

# Define output filename and save the image
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")