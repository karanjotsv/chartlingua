import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare Data for Plotly ---
categories = [item['category'] for item in chart_data]
series_names = texts.get('legend_labels', [])

data_series = {}
for series_name in series_names:
    data_series[series_name] = [item['values'].get(series_name) for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

for i, series_name in enumerate(series_names):
    fig.add_trace(go.Bar(
        x=categories,
        y=data_series[series_name],
        name=series_name,
        marker_color=colors[i],
        text=data_series[series_name],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white',
            weight='bold'
        ),
        hoverinfo='skip'
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        linecolor='#d9d9d9',
        tickfont=dict(color='#666666')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#e9e9e9',
        zeroline=False,
        range=[0, 50000],
        tickvals=[0, 10000, 20000, 30000, 40000, 50000],
        tickfont=dict(color='#666666')
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font=dict(size=14)
    ),
    showlegend=True
)

# Add annotations for source and notes
if texts.get('note'):
    fig.add_annotation(
        text=texts['note'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.25,
        xanchor='left',
        yanchor='bottom',
        font=dict(color='#146EC0', size=12)
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.25,
        xanchor='right',
        yanchor='bottom',
        font=dict(color='#666666', size=12)
    )

# --- 5. Output the Image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")