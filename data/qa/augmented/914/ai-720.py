import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided
if len(sys.argv) != 2:
    # Minimal error message as per instructions
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text elements from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series_list = data['series']

# Initialize the Plotly figure
fig = go.Figure()

# Add alternating background color bands for visual structure
for year in range(1987, max(categories) + 1, 4):
    fig.add_shape(
        type="rect",
        xref="x", yref="paper",
        x0=year, y0=0, x1=year + 2, y1=1,
        fillcolor="#fafafa",
        layer="below",
        line_width=0
    )

# Iterate through the series data to plot traces
for i, series in enumerate(series_list):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series['data'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=5),
        hoverinfo='none'
    ))

# Add data point labels as annotations
for series in series_list:
    if 'labels' in series and 'label_positions' in series:
        for x_val, y_val, label, pos in zip(categories, series['data'], series['labels'], series['label_positions']):
            if label is not None and pos is not None:
                yshift = 8 if pos == 'top' else -8
                yanchor = 'bottom' if pos == 'top' else 'top'
                fig.add_annotation(
                    x=x_val, y=y_val, text=str(label),
                    showarrow=False,
                    font=dict(family="Arial", size=11, color='#333333'),
                    xanchor='center',
                    yanchor=yanchor,
                    yshift=yshift
                )

# Configure the chart's layout, axes, and other visual elements
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=1985,
        dtick=2,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 150],
        tickmode='linear',
        dtick=25,
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=80, r=20, t=20, b=80),
    height=600,
    width=900
)

# Add the source text as an annotation at the bottom-right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        xanchor='right',
        yanchor='top',
        showarrow=False,
        font=dict(family="Arial", size=12, color="grey")
    )

# Determine the output filename from the input JSON path
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + ".png"
else:
    output_filename = json_path + ".png"

# Save the generated figure to a PNG file with a high scale for better resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")