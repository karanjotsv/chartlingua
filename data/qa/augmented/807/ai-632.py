import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Unpack Data and Texts ---
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
legend_items = texts['legend_items']

categories = [item['category'] for item in chart_data]
# Transpose the list of value lists into separate lists for each series
series_values = list(zip(*[item['values'] for item in chart_data]))

# --- 3. Create Chart ---
fig = go.Figure()

# Add a trace for each data series, iterating in order
for i, series_name in enumerate(legend_items):
    values = series_values[i]
    
    # Format text labels: bold, space as thousand separator, and hide for zero values
    text_labels = [f"<b>{f'{v:,}'.replace(',', ' ')}</b>" if v > 0 else '' for v in values]

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        name=series_name,
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(width=0)
        ),
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            color='white'
        )
    ))

# --- 4. Configure Layout ---
fig.update_layout(
    barmode='stack',
    font=dict(
        family="Arial",
        size=12,
        color='#333333'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        ticks='outside',
        tickcolor='#cccccc'
    ),
    yaxis=dict(
        showgrid=False,
        autorange='reversed'  # Ensures the first item in the data appears at the top
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=150, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='auto',
            font=dict(size=12, color='#666666')
        )
    ]
)

# --- 5. Output to PNG ---
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")