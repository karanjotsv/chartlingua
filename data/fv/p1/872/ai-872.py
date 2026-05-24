import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

# Find data series by name
historical_data = next((item for item in data if item["name"] == "Historical"), None)
planned_data = next((item for item in data if item["name"] == "Planned"), None)
trendline_data = next((item for item in data if item["name"] == "Trendline"), None)

# Add Trendline trace
if trendline_data:
    fig.add_trace(go.Scatter(
        x=trendline_data['x'],
        y=trendline_data['y'],
        mode='lines',
        name=texts['legend_trendline'],
        line=dict(color='white', width=5, dash='dot')
    ))

# Add Historical trace
if historical_data:
    fig.add_trace(go.Scatter(
        x=historical_data['x'],
        y=historical_data['y'],
        mode='lines+markers',
        name=historical_data['name'],
        line=dict(color=colors[0], width=3),
        marker=dict(color='black', size=8),
        showlegend=False
    ))

# Add Planned trace
if planned_data:
    fig.add_trace(go.Scatter(
        x=planned_data['x'],
        y=planned_data['y'],
        mode='lines+markers',
        name=texts['legend_planned'],
        line=dict(color=colors[1], width=3),
        marker=dict(color='#FFFF00', size=8, line=dict(color='black', width=1))
    ))

# Add annotations for data point labels
all_series_with_labels = [s for s in [historical_data, planned_data] if s and 'labels' in s]
for series in all_series_with_labels:
    for i, label_info in enumerate(series['labels']):
        fig.add_annotation(
            x=series['x'][i],
            y=series['y'][i],
            text=label_info['text'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='black'),
            ax=label_info['ax'],
            ay=label_info['ay'],
            align='center'
        )

# Add other annotations (including arrowed ones)
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=ann.get('showarrow', False),
        arrowhead=2 if ann.get('showarrow', False) else 0,
        arrowcolor='black',
        arrowsize=1.5,
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        font=dict(family="Arial", size=12, color='black'),
        align='center'
    )

# Add horizontal background bands
y_ticks_log = list(range(10, 22))
for i in range(len(y_ticks_log) -1):
    if i % 2 == 1:
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=10**y_ticks_log[i],
            x1=1, y1=10**y_ticks_log[i+1],
            line_width=0,
            fillcolor="rgba(128, 128, 128, 0.1)",
            layer="below"
        )
        
# Set layout and styling
fig.update_layout(
    font=dict(family="Arial", size=12),
    paper_bgcolor='#333333',
    plot_bgcolor='#EBE0D5',
    margin=dict(l=80, r=40, t=120, b=100),
    xaxis=dict(
        title=texts['x_axis_title'],
        range=[1990, 2030],
        dtick=5,
        showgrid=True,
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type='log',
        range=[10, 21],
        tickvals=[10**i for i in range(10, 22)],
        ticktext=[f"10<sup>{i}</sup>" for i in range(10, 22)],
        showgrid=True,
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    legend=dict(
        x=0.98, y=0.4,
        xanchor='right', yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.6)',
        bordercolor='black',
        borderwidth=1,
        font=dict(color='black')
    ),
    annotations=[
        # Main Title
        dict(
            text=f"<b>{texts['title']}</b>",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=24, color='#FFFF00')
        ),
        # Subtitle with background box
        dict(
            text=f"{texts['subtitle']}",
            xref="paper", yref="paper",
            x=0.5, y=0.92,
            xanchor='center', yanchor='bottom',
            showarrow=False,
            font=dict(family="Arial", size=16, color='black'),
            bgcolor='white',
            borderpad=4
        ),
        # Source Note
        dict(
            text=texts['source_note'],
            xref="paper", yref="paper",
            x=0.5, y=-0.15,
            xanchor='center', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=12, color='black')
        )
    ]
)

# Generate output PNG
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")