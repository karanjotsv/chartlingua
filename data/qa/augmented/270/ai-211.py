import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python your_script_name.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Format text for bar labels to use a space as a thousands separator
bar_texts = [f'{val:,}'.replace(',', ' ') for val in y_values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=bar_texts,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title=texts['yaxis_title'],
        title_font=dict(size=14),
        range=[0, 1500],
        tickmode='array',
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500],
        ticktext=['0', '250', '500', '750', '1 000', '1 250', '1 500'],
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        ticks=''
    ),
    xaxis=dict(
        title=texts['xaxis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickcolor='black'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='top',
        font=dict(size=12)
    )

# Derive output filename from the input JSON path without using 'os' module
sanitized_path = json_path.replace('\\', '/')
base_filename = sanitized_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")