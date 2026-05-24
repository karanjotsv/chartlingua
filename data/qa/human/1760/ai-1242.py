import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract and prepare data ---
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Extract data for plotting, and reverse for correct order in horizontal bar chart
categories = [item['category'] for item in chart_data]
series1_values = [item['values'][0] for item in chart_data]
series2_values = [item['values'][1] for item in chart_data]

categories.reverse()
series1_values.reverse()
series2_values.reverse()

# --- 3. Create the figure ---
fig = go.Figure()

# Add the two bar traces for the stacked bar chart
fig.add_trace(go.Bar(
    y=categories,
    x=series1_values,
    name=texts['series_labels'][0],
    orientation='h',
    marker=dict(color=colors['series_colors'][0], line=dict(width=0)),
    hoverinfo='none'
))

fig.add_trace(go.Bar(
    y=categories,
    x=series2_values,
    name=texts['series_labels'][1],
    orientation='h',
    marker=dict(color=colors['series_colors'][1], line=dict(width=0)),
    hoverinfo='none'
))

# --- 4. Configure layout and annotations ---
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
source_text = f"{texts['source']}<br><b>{texts['note']}</b>"

# This list will hold all our custom text annotations
annotations = []

# Add annotations for category labels and data values in columns
for i, category in enumerate(categories):
    # Category labels on the far left
    annotations.append(dict(
        xref='paper', yref='y',
        x=0.01, y=category,
        text=category,
        font=dict(family='Arial', size=14),
        showarrow=False, align='left', xanchor='left'
    ))
    # Series 1 ("Bad") values
    annotations.append(dict(
        xref='paper', yref='y',
        x=0.29, y=category,
        text=str(series1_values[i]),
        font=dict(family='Arial', size=14),
        showarrow=False, align='right', xanchor='right'
    ))
    # Series 2 ("Good") values
    annotations.append(dict(
        xref='paper', yref='y',
        x=0.81, y=category,
        text=str(series2_values[i]),
        font=dict(family='Arial', size=14),
        showarrow=False, align='left', xanchor='left'
    ))

# Add headers for "Bad" and "Good" columns
# These are positioned relative to the bar chart's domain
domain_start = 0.3
domain_end = 0.8
domain_width = domain_end - domain_start
max_x_val = 100 # Assume percentage scale for positioning

# Position "Bad" header over the average center of the first bar segment
avg_series1_center = sum(series1_values) / len(series1_values) / 2
bad_header_pos = domain_start + (avg_series1_center / max_x_val) * domain_width
annotations.append(dict(
    xref='paper', yref='paper',
    x=bad_header_pos, y=1.02,
    text=f"<b>{texts['series_labels'][0]}</b>",
    font=dict(family='Arial', size=14),
    showarrow=False, xanchor='center', yanchor='bottom'
))

# Position "Good" header over the average center of the second bar segment
avg_series2_midpoint = sum(s1 + s2/2 for s1, s2 in zip(series1_values, series2_values)) / len(series1_values)
good_header_pos = domain_start + (avg_series2_midpoint / max_x_val) * domain_width
annotations.append(dict(
    xref='paper', yref='paper',
    x=good_header_pos, y=1.02,
    text=f"<b>{texts['series_labels'][1]}</b>",
    font=dict(family='Arial', size=14),
    showarrow=False, xanchor='center', yanchor='bottom'
))

# Add source annotation
annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=-0.15,
    text=source_text,
    showarrow=False, align='left', xanchor='left', yanchor='top',
    font=dict(family='Arial', size=12)
))


fig.update_layout(
    barmode='stack',
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14),
    margin=dict(l=20, r=20, t=120, b=100, pad=10),
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        domain=[domain_start, domain_end],
        range=[0, max_x_val]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        categoryorder='array',
        categoryarray=categories
    ),
    annotations=annotations
)

# --- 5. Output the image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")