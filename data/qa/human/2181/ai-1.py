import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in s['data']],
        textposition='inside',
        textfont=dict(
            family="Arial",
            size=14,
            color='white'
        ),
        insidetextfont=dict(
             family="Arial",
             size=14,
             color='white'
        ),
        hovertemplate='%{y}%<extra></extra>'
    ))

# Update layout for a stacked bar chart appearance
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickfont=dict(size=12),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 125],
        dtick=25,
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    # Add source annotation
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.3,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Update text on bars to be bold
fig.update_traces(
    texttemplate='<b>%{text}</b>'
)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"


# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")