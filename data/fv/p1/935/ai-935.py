import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0, 0.65])
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=0.7,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=50, r=50, t=80, b=180),
    annotations=[
        dict(
            text=texts['source_left'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            align='left'
        ),
        dict(
            text=texts['source_right'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            align='right'
        )
    ]
)

# Determine output filename and save the image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")