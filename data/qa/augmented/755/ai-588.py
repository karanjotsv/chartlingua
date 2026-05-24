import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = pathlib.Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Unpack data and configuration ---
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text:,}'.replace(',', ' '),
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", color='black')
))

# --- 4. Configure layout ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=180, r=60, t=50, b=100),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        range=[0, 30000],
        zeroline=False,
        showline=False,
        ticks='outside',
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000],
        ticktext=['0', '5 000', '10 000', '15 000', '20 000', '25 000', '30 000']
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        categoryorder='total ascending' # Ensures the order from JSON is respected
    ),
    annotations=[] # Placeholder for source text
)

# Add source annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0.98, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12)
    )

# --- 5. Save the figure to a file ---
output_filename = json_filepath.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")