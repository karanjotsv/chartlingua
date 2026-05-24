import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data.get('series', [])):
    fig.add_trace(go.Bar(
        y=data.get('categories', []),
        x=series.get('values', []),
        name=series.get('name', ''),
        orientation='h',
        marker=dict(color=colors[i]),
        text=series.get('values', []),
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white',
            weight='bold'
        )
    ))

# Update layout for a professional appearance
fig.update_layout(
    barmode='stack',
    title=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 255] # Set range to match the original chart's scale
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    margin=dict(l=250, r=20, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.2,
            align='right',
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# Generate the output filename from the input JSON path
output_path = pathlib.Path(json_path).with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")