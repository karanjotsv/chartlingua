import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract data and texts ---
categories = chart_data['chart_data']['categories']
series_data = chart_data['chart_data']['series']
texts = chart_data['texts']
colors = chart_data['colors']

# --- 3. Create the figure ---
fig = go.Figure()

# --- 4. Add traces for each data series ---
for i, series in enumerate(series_data):
    # Format text labels to match the original chart (bold, with percentage sign)
    # The original chart has inconsistencies in decimal places (e.g., "8%").
    # This loop dynamically formats based on whether the number is an integer.
    text_labels = []
    for v in series['data']:
        if v == int(v):
            label = f"<b>{int(v)}%</b>"
        else:
            label = f"<b>{v}%</b>"
        text_labels.append(label)

    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors['bar_colors'][i],
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color=colors['text_colors'][i]
        )
    ))

# --- 5. Configure layout ---
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=70, r=40, b=120, t=40),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=categories,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 100],
        tickvals=[0, 20, 40, 60, 80],
        showgrid=True,
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# --- 6. Output the image ---
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved as {output_filename}")