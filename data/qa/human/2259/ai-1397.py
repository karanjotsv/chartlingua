import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Initialize figure
fig = go.Figure()

# Extract data for plotting
categories = chart_data['categories']
series_data = chart_data['chart_data']
colors = chart_data['colors']
texts = chart_data['texts']

# Add bar traces for each series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    barmode='group',
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showticklabels=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        griddash='dash',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    shapes=[
        dict(
            type="line",
            xref="paper",
            yref="paper",
            x0=0.5,
            y0=0,
            x1=0.5,
            y1=1,
            line=dict(
                color="lightgray",
                width=1,
                dash="dash",
            )
        )
    ]
)

# Combine and add annotations for title and source
# Since there's no main title, we only add the source annotation.
annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            xref="paper", yref="paper",
            x=0.98, y=-0.4,
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='grey'),
            align='right'
        )
    )

fig.update_layout(annotations=annotations)


# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")