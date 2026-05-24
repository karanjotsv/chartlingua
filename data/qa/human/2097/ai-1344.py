import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

# Extract data for plotting
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False,
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 85],
        tickvals=[0, 20, 40, 60, 80],
        ticktext=['0%', '20%', '40%', '60%', '80%'],
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        automargin=True
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.35,
        xanchor='center',
        x=0.5
    ),
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=70, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.45,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                family="Arial",
                size=12,
                color='grey'
            )
        )
    ] if texts.get('source') else []
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")