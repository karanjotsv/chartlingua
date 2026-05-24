import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize a Plotly Figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=s['data'],
        mode='lines',
        name=s.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5)
    ))

# Configure the chart layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=20, color='black')
    ),
    xaxis=dict(
        title=dict(text=texts['x_axis_title'], font=dict(family="Arial", size=14)),
        tickmode='linear',
        tick0=1900,
        dtick=10,
        range=[1899, 2008],
        showgrid=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title=dict(text="", font=dict(family="Arial", size=14)), # Title added via annotation
        tickmode='linear',
        tick0=0,
        dtick=100,
        range=[0, 800],
        showgrid=True,
        gridcolor='#A9A9A9',
        gridwidth=1,
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80)
)

# Add a custom annotation for the horizontal Y-axis title
fig.add_annotation(
    text=texts['y_axis_title'],
    align='center',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.01,
    y=0.99,
    xanchor='left',
    yanchor='top',
    font=dict(family="Arial", size=14)
)

# Determine the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")