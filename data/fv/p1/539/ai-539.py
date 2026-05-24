import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
        
    filename_base = os.path.splitext(os.path.basename(json_path))[0]

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    fig = go.Figure()

    # Main donut chart
    main_data = config['chart_data']['main_chart']
    fig.add_trace(go.Pie(
        labels=main_data['labels'],
        values=main_data['values'],
        hole=0.6,
        marker_colors=config['colors'],
        textinfo='none',
        hoverinfo='none',
        sort=False,
        direction='clockwise',
        domain={'y': [0.4, 0.95]}
    ))

    # Sub-charts
    sub_charts_data = config['chart_data']['sub_charts']
    num_sub_charts = len(sub_charts_data)
    sub_chart_width = 0.12
    gap = 0.04
    total_width = num_sub_charts * sub_chart_width + (num_sub_charts - 1) * gap
    start_x = (1 - total_width) / 2
    
    sub_chart_y_domain = [0.18, 0.33]

    for i, chart in enumerate(sub_charts_data):
        x_start = start_x + i * (sub_chart_width + gap)
        x_end = x_start + sub_chart_width
        fig.add_trace(go.Pie(
            values=[chart['value'], 100 - chart['value']],
            hole=0.6,
            marker_colors=config['colors'],
            textinfo='none',
            hoverinfo='none',
            sort=False,
            direction='clockwise',
            domain={'x': [x_start, x_end], 'y': sub_chart_y_domain}
        ))
        
        # Add annotation for percentage above sub-chart
        fig.add_annotation(
            x=(x_start + x_end) / 2,
            y=sub_chart_y_domain[1] + 0.04,
            text=f"{chart['value']}%",
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            xref="paper",
            yref="paper"
        )
        
        # Add annotation for label inside sub-chart
        fig.add_annotation(
            x=(x_start + x_end) / 2,
            y=(sub_chart_y_domain[0] + sub_chart_y_domain[1]) / 2,
            text=chart['label'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            xref="paper",
            yref="paper"
        )

    # Annotations for main chart
    fig.add_annotation(
        text=config['texts']['main_chart_center_text'],
        x=0.5, y=0.675,
        font=dict(family="Arial", size=16, color='black'),
        showarrow=False,
        xref="paper", yref="paper"
    )
    
    fig.add_annotation(
        text=config['texts']['main_chart_labels']['yes'],
        x=0.5, y=0.89,
        font=dict(family="Arial", size=14, color='white'),
        showarrow=False,
        xref="paper", yref="paper"
    )
    
    fig.add_annotation(
        text=config['texts']['main_chart_labels']['no'],
        x=0.8, y=0.55,
        font=dict(family="Arial", size=16, color='black'),
        showarrow=False,
        xref="paper", yref="paper"
    )

    # General layout settings
    fig.update_layout(
        title_text=config['texts']['title'],
        title_font=dict(family="Arial", size=18, color='black'),
        title_x=0.02,
        title_y=0.98,
        title_xanchor='left',
        title_yanchor='top',
        
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        
        font=dict(family="Arial"),
        
        margin=dict(l=20, r=20, t=80, b=250),
        width=600,
        height=900
    )
    
    # Source text annotation
    fig.add_annotation(
        text=config['texts']['source'],
        showarrow=False,
        xref='paper', yref='paper',
        x=0.02, y=0.01,
        xanchor='left', yanchor='bottom',
        align='left',
        font=dict(family="Arial", size=10, color='black')
    )

    fig.write_image(f"{filename_base}.png", scale=2)
    print(f"Chart saved to {filename_base}.png")

if __name__ == "__main__":
    main()