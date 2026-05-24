import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
x_values = chart_data['x_values']

# Initialize a Plotly Figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series['y_values'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=7),
        text=[f'{v:,}'.replace(',', ' ') for v in series['y_values']],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='#000000'
        )
    ))

# Update the layout of the chart for a professional appearance
fig.update_layout(
    font=dict(family="Arial", size=12, color='#1f2937'),
    plot_bgcolor='white',
    xaxis=dict(
        tickvals=x_values,
        tickformat='%Y',
        showgrid=True,
        gridcolor='#e5e7eb',
        linecolor='#6b7280',
        showline=True,
        zeroline=False
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 85000],
        tickvals=[i for i in range(0, 80001, 10000)],
        ticktext=[f'{v:,}'.replace(',', ' ') for v in range(0, 80001, 10000)],
        showgrid=True,
        gridcolor='#e5e7eb',
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[]
)

# Add source annotation if it exists in the JSON
if texts.get('source'):
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0.99, y=-0.35,
        text=texts['source'],
        showarrow=False,
        xanchor='right', yanchor='bottom',
        font=dict(size=12, color='#6b7280')
    )

# Generate the output filename from the input JSON path
output_filename_base = json_file_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")