import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create a figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        y=chart_data['categories'],
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='black', width=0)
        ),
        text=series['values'],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

# Update layout to match the original chart's style
fig.update_layout(
    barmode='group',
    title=dict(
        text=texts['title'],
        font=dict(family='Arial', size=24, color='black'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        range=[0, 6],
        showgrid=True,
        gridcolor='white',
        zeroline=False,
        tickfont=dict(family='Arial'),
        linecolor='grey'
    ),
    yaxis=dict(
        autorange='reversed',
        showline=True,
        linecolor='black',
        linewidth=2,
        ticks='',
        gridcolor='rgba(0,0,0,0)',
        tickfont=dict(family='Arial')
    ),
    plot_bgcolor='#e0e0e0',
    paper_bgcolor='#e0e0e0',
    font=dict(family="Arial"),
    margin=dict(l=150, r=40, t=100, b=80),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    )
)

# Derive output filename from the input JSON filename
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for image export.")
    sys.exit(1)