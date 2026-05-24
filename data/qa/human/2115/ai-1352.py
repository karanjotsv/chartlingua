import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
    
# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i]),
        marker=dict(color=colors[i], size=6),
        text=[f'{val:.2f}' for val in series['y']],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        )
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'],
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        tickmode='array',
        tickvals=chart_data[0]['x'],
        ticktext=[str(year) for year in chart_data[0]['x']],
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        range=[68, 81],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        linecolor='black'
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.28,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")