import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure object
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        texttemplate='<b>%{text:,}</b>',
        insidetextanchor='middle',
        textfont=dict(
            color='white',
            family='Arial',
            size=14
        )
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    yaxis=dict(
        range=[0, 15000],
        dtick=2500,
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=chart_data[0]['x'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=80, r=40, t=40, b=120)
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.3,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color="#888888")
    )

# Generate the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")