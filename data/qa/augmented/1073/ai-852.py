import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data and texts from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    cliponaxis=False,
    insidetextanchor='start' # Not strictly needed but can help with positioning
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=50, t=50, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickformat=',.0f',
        ticks='outside'
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        ticklen=5
    )
)

# Add source and note annotations
if texts.get('note'):
    fig.add_annotation(
        text=f"<b>ⓘ</b> {texts['note']}",
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(color="#007bff")
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top'
    )

# Determine output filename and save the image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")