import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the chart data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# Initialize the Plotly figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_data):
    # Format text labels to be bold and include a percentage sign
    bar_texts = [f"<b>{val}%</b>" for val in series['data']]
    
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['data'],
        marker_color=colors[i],
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color='white'
        )
    ))

# Add faint vertical lines between the categories to match the original chart style
for i in range(len(categories) - 1):
    fig.add_vline(x=i + 0.5, line_width=1, line_dash="solid", line_color="lightgray")

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=40, t=50, b=150),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 101],
        tickvals=[0, 25, 50, 75, 100],
        ticktext=['0%', '25%', '50%', '75%', '100%'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    xaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=False,
        ticks='outside'
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    annotations=[]
)

# Add source text annotation if it exists in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.28,
        font=dict(size=10)
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")