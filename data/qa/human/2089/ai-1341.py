import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data, texts, and colors from the JSON object
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors['bar_colors'][i],
        texttemplate='%{y:.2f}%',
        textposition='inside',
        textfont_color=colors['text_font_colors'][i],
        insidetextanchor='middle'
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    template='plotly_white',
    font=dict(family="Arial"),
    title=dict(text=texts['title']),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickmode='array',
        tickvals=data_series[0]['x'],
        ticktext=[str(year) for year in data_series[0]['x']]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=120)
)

# Add source annotation
fig.add_annotation(
    text=texts['source'],
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1.0,
    y=-0.3,
    xanchor='right',
    yanchor='bottom',
    font=dict(size=12, color='#808080')
)


# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")