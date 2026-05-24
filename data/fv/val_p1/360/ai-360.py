import sys
import json
import pathlib
import plotly.graph_objects as go

# Read JSON data from the command-line argument
json_path = pathlib.Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
pie_texts = [item['label_text'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=pie_texts,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(colors=colors, line=dict(color='black', width=1.5)),
    sort=False,
    direction='clockwise',
    rotation=90
)])

# Update layout properties
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(family="Arial", size=24, color='black'),
    font=dict(family="Arial", size=14, color='black'),
    showlegend=True,
    legend=dict(
        traceorder="normal",
        font=dict(family="Arial", size=12, color='black')
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=120, b=40),
    width=800,
    height=600
)

# Use 'auto' to let Plotly decide whether to place text inside or outside
fig.update_traces(textposition='auto')

# Generate and save the output image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)