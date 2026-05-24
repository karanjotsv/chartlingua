import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data series for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,  # Prevents text on the highest bar from being clipped
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Combine source and note for the annotation
source_text = texts.get('source', '') or ''
note_text = texts.get('note', '') or ''
if source_text and note_text:
    source_display_text = f"{source_text}<br>{note_text}"
else:
    source_display_text = source_text or note_text

# Update the figure layout for a clean, professional appearance
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 105], # Provides padding for the top data label
        tickmode='linear',
        tick0=0,
        dtick=20,
        linecolor='black',
        ticks='outside'
    ),
    margin=dict(l=80, r=40, t=40, b=80),
)

# Add an annotation for the source text if it exists
if source_display_text:
    fig.add_annotation(
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.20,
        xanchor='right',
        yanchor='top',
        text=source_display_text,
        font=dict(
            family="Arial",
            size=10,
            color='grey'
        )
    )

# Determine the output filename from the input JSON path
base_name = json_path.rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
output_filename = base_name.rsplit('.', 1)[0] + '.png'

# Write the figure to a high-resolution PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")