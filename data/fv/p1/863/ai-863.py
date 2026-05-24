import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data and texts
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']
special_elements = chart_spec.get('special_elements', {})

# Create the figure
fig = go.Figure()

# Add data series to the chart
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2.5)
    ))

# Add special elements like vertical lines and custom labels
if 'vertical_lines' in special_elements:
    for line in special_elements['vertical_lines']:
        fig.add_shape(
            type='line',
            x0=line['x'], y0=0,
            x1=line['x'], y1=line['y_max'],
            line=dict(color='black', width=2)
        )

if 'x_axis_labels' in special_elements:
    for label in special_elements['x_axis_labels']:
        fig.add_annotation(
            x=label['x'],
            y=0,
            text=label['text'],
            showarrow=True,
            arrowhead=0, # No arrowhead, just a line
            arrowcolor='black',
            ax=0,
            ay=20, # Length of the pointer line
            yshift=-35, # Move text down
            font=dict(family="Arial", size=12, color="black"),
            align='center'
        )
        # Add small horizontal ticks for the bracket effect
        fig.add_shape(type='line', x0=label['x']-0.2, y0=-0.03, x1=label['x']+0.2, y1=-0.03, line=dict(color='black', width=1.5))
        fig.add_shape(type='line', x0=label['x']-0.2, y0=0, x1=label['x']-0.2, y1=-0.03, line=dict(color='black', width=1.5))
        fig.add_shape(type='line', x0=label['x']+0.2, y0=0, x1=label['x']+0.2, y1=-0.03, line=dict(color='black', width=1.5))


# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'],
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-0.5, 26] # Give some padding
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 1.05],
        tickmode='array',
        tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        ticks='outside'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5,
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=80, r=40, b=120, t=40)
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")