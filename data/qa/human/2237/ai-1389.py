import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create figure
fig = go.Figure()

# Add traces for each series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{y}%' for y in series['data']],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family='Arial', size=12, color='black')
    ))

# Update layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 50],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        title_standoff=15
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.32,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='#555555')
        )
    ]
)

# Generate output filename from JSON path
output_filename = json_path.with_suffix('.png')

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")