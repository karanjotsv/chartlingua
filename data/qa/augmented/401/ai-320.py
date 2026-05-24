import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add data series (bars) to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        text=series.get('y'),
        texttemplate='%{text: }',  # Format numbers with space as thousands separator
        textposition='outside',
        marker_color=colors[i % len(colors)] if colors else None,
        cliponaxis=False  # Prevent text labels from being clipped by the plot area
    ))

# Combine source and note for the annotation, handling null values
source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
# The note is styled to look like a link, as in the source image
if texts.get('note'):
    source_note_parts.append(f"<span style='color:#0066cc;'>{texts['note']}</span>")
source_note_html = "<br>".join(source_note_parts)

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='#cccccc',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 3000],
        dtick=500,
        tickformat=' ',  # Use space as thousands separator for axis labels
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=60, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=source_note_html,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Update trace properties globally
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

# Derive the output filename from the input JSON file path
# e.g., "path/to/my_chart.json" -> "my_chart.png"
base_filename = json_path.split('/')[-1].split('.')[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")