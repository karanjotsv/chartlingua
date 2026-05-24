import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
legend_labels = texts['legend_labels']

categories = [item['category'] for item in data]
values_by_series = [[item['values'][i] for item in data] for i in range(len(legend_labels))]

# Create the figure object
fig = go.Figure()

# Add a bar trace for each data series
for i, label in enumerate(legend_labels):
    fig.add_trace(go.Bar(
        x=categories,
        y=values_by_series[i],
        name=label,
        marker_color=colors[i]
    ))

# Update layout for a professional appearance
fig.update_layout(
    barmode='stack',
    font_family='Arial',
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        categoryorder='array',
        categoryarray=categories,
        showgrid=True,
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 1050000],
        tickvals=[0, 250000, 500000, 750000, 1000000],
        ticktext=["0", "250 000", "500 000", "750 000", "1 000 000"],
        showgrid=True,
        gridcolor='#dddddd'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=40, pad=4),
    annotations=[]
)

# Add source annotation if present
if texts.get('source'):
    fig.layout.annotations += (dict(
        text=texts['source'],
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=12)
    ),)

# Generate the output image file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")