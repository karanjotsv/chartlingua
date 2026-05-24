import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_image_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Prepare Data for Plotting ---
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
series_names = config['series_names']

categories = [item['category'] for item in chart_data]
values_s1 = [item['values'][0] for item in chart_data]
values_s2 = [item['values'][1] for item in chart_data]

# Add gaps to create visual grouping
y_labels_with_gaps = categories[0:1] + [''] + categories[1:4] + [''] + categories[4:6]
x_s1_with_gaps = values_s1[0:1] + [None] + values_s1[1:4] + [None] + values_s1[4:6]
x_s2_with_gaps = values_s2[0:1] + [None] + values_s2[1:4] + [None] + values_s2[4:6]
all_x_series = [x_s1_with_gaps, x_s2_with_gaps]

# Create text labels for bars (add '%' only for 'Total' category)
text_labels_s1 = [f"{v}%" if c == "Total" else str(v) for v, c in zip(values_s1, categories)]
text_labels_s2 = [f"{v}%" if c == "Total" else str(v) for v, c in zip(values_s2, categories)]
text_s1_with_gaps = text_labels_s1[0:1] + [None] + text_labels_s1[1:4] + [None] + text_labels_s1[4:6]
text_s2_with_gaps = text_labels_s2[0:1] + [None] + text_labels_s2[1:4] + [None] + text_labels_s2[4:6]
all_text_series = [text_s1_with_gaps, text_s2_with_gaps]

# Reverse order for Plotly's default bottom-to-top rendering
y_labels = y_labels_with_gaps[::-1]
for i in range(len(all_x_series)):
    all_x_series[i] = all_x_series[i][::-1]
    all_text_series[i] = all_text_series[i][::-1]

# --- 3. Create Figure ---
fig = go.Figure()

# Add traces for each data series
for i, series_name in enumerate(series_names):
    fig.add_trace(go.Bar(
        y=y_labels,
        x=all_x_series[i],
        name=series_name,
        orientation='h',
        marker=dict(color=colors[i], line_width=0),
        text=all_text_series[i],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial', size=14),
        hoverinfo='none'
    ))

# --- 4. Configure Layout and Styling ---
title_text = f"<span style='font-size:22px;'><b>{texts['title']}</b></span><br><span style='font-size:16px;color:#555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01, y=0.98,
        xanchor='left', yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[0, 105]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=40, t=140, b=150),
    showlegend=False,
    height=600
)

# Add custom y-axis labels as annotations for left alignment
for i, label in enumerate(y_labels):
    if label:
        fig.add_annotation(
            text=label,
            xref='paper', yref='y',
            x=-0.01, y=i,
            xanchor='right', yanchor='middle',
            align='right',
            showarrow=False,
            font=dict(size=14)
        )

# Add source/note text at the bottom
fig.add_annotation(
    text=texts['source_note'],
    align='left',
    showarrow=False,
    xref='paper', yref='paper',
    x=0, y=0,
    xanchor='left', yanchor='top',
    yshift=-30 # Shift down from the bottom of plotting area
)

# Add custom legend headers ("Bad", "Good") above the first bar
total_y_pos = y_labels.index("Total")
total_vals = chart_data[0]['values']
x_pos_bad = total_vals[0] / 2
x_pos_good = total_vals[0] + total_vals[1] / 2

fig.add_annotation(
    text="<b>Bad</b>",
    xref='x', yref='y',
    x=x_pos_bad, y=total_y_pos,
    yshift=25,
    showarrow=False,
    font=dict(size=14, color='black')
)

fig.add_annotation(
    text="<b>Good</b>",
    xref='x', yref='y',
    x=x_pos_good, y=total_y_pos,
    yshift=25,
    showarrow=False,
    font=dict(size=14, color='black')
)

# --- 5. Export Image ---
fig.write_image(str(output_image_path), scale=2)
print(f"Chart saved to {output_image_path}")