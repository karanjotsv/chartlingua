import sys
import json
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])
bar_colors = colors.get('bar_colors', [])
text_colors = colors.get('text_colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series, ensuring data order is preserved
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=bar_colors[i] if i < len(bar_colors) else None,
        text=series.get('data', []),
        textposition='inside',
        texttemplate='%{text}',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color=text_colors[i] if i < len(text_colors) else 'black'
        )
    ))

# Update layout for a clean and accurate presentation
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=20,
        range=[0, 301],
        dtick=50,
        showgrid=True,
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    showlegend=True
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.98, y=-0.3,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(family="Arial", size=10, color="grey")
    )

# Determine the output filename from the input JSON path
base_filename = json_path.split('/')[-1].split('.')[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")