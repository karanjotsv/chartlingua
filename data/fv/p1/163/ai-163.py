import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_chart(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']
    
    fig = make_subplots(
        rows=3, cols=2,
        specs=[
            [{"colspan": 2, "rowspan": 1}, None],
            [{"colspan": 2, "rowspan": 1}, None],
            [{}, {}]
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # --- Top Plot: Navigation Paths ---
    path_plot_data = data['path_plot']['series']
    for i, series in enumerate(path_plot_data):
        fig.add_trace(
            go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                line=dict(color=colors[i], width=2),
                name=series['name'],
                showlegend=False
            ),
            row=1, col=1
        )
        
    for ann in data['path_plot']['annotations']:
        fig.add_annotation(
            x=ann['x'], y=ann['y'], text=ann['text'],
            showarrow=False, font=dict(color='white', size=12),
            row=1, col=1
        )
    
    fig.add_annotation(
        x=20, y=-57.5, text="Mean",
        showarrow=False, font=dict(color='white', size=12),
        row=1, col=1, xshift=10
    )


    # --- Middle Plot: Normalized to "Mean" ---
    normalized_data = data['normalized_plot']['series']
    for i, series in enumerate(normalized_data):
        fig.add_trace(
            go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=1),
                showlegend=False
            ),
            row=2, col=1
        )
    fig.add_shape(type="line", x0=-0.5, y0=0, x1=10.5, y1=0,
                  line=dict(color="white", width=2), row=2, col=1)

    # --- Bottom-Left Plot: Daily Distance Error ---
    dist_error_data = data['distance_error_scatter']
    scatter_colors = [colors[i % (len(colors)-1)] for i in range(len(dist_error_data['x']))] # exclude white
    fig.add_trace(
        go.Scatter(
            x=dist_error_data['x'],
            y=dist_error_data['y'],
            mode='markers',
            marker=dict(color=scatter_colors, size=4),
            showlegend=False
        ),
        row=3, col=1
    )

    # --- Bottom-Right Plot: Daily Course Error ---
    course_error_data = data['course_error_scatter']
    fig.add_trace(
        go.Scatter(
            x=course_error_data['x'],
            y=course_error_data['y'],
            mode='markers',
            marker=dict(color=scatter_colors, size=4),
            showlegend=False
        ),
        row=3, col=2
    )

    # --- Layout and Styling ---
    fig.update_layout(
        title=dict(
            text=f"<b>{texts['title']}</b>",
            font=dict(size=24, color='white'),
            x=0.5, y=0.97, xanchor='center', yanchor='top'
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Arial", color='white', size=12),
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=False,
        height=800,
        width=1000
    )

    # --- Axis Configuration ---
    # Top plot axes
    fig.update_xaxes(row=1, col=1, visible=False, range=[0, 60])
    fig.update_yaxes(
        row=1, col=1, 
        range=[-59.5, -53.5], 
        tickvals=[-59, -58, -57, -56, -55, -54],
        ticktext=texts['y_axis_labels_top'],
        gridcolor='rgba(255, 255, 255, 0.3)',
        zeroline=False
    )
    
    # Middle plot axes
    fig.update_xaxes(row=2, col=1, visible=False)
    fig.update_yaxes(row=2, col=1, visible=False)
    
    # Bottom-left axes
    fig.update_xaxes(row=3, col=1, tickvals=[100, 200], ticktext=texts['distance_error_x_labels'], showgrid=False, zerolinecolor='white', zerolinewidth=1)
    fig.update_yaxes(row=3, col=1, tickvals=[50, 100], ticktext=[texts['scatter_y_label_50'], texts['scatter_y_label_100']], range=[0, 105])

    # Bottom-right axes
    fig.update_xaxes(row=3, col=2, tickvals=[30, 60, 90, 120], ticktext=texts['course_error_x_labels'], showgrid=False, zerolinecolor='white', zerolinewidth=1)
    fig.update_yaxes(row=3, col=2, tickvals=[50, 100], ticktext=[texts['scatter_y_label_50'], texts['scatter_y_label_100']], range=[0, 105])
    
    # --- Annotations (Titles, Legends, etc.) ---
    
    # Legend annotations for top plot
    legend_texts = texts['legend_captions']
    for i in range(3):
        fig.add_annotation(x=0.01, y=1-0.03*i, text=legend_texts[i], font=dict(color=colors[i]), showarrow=False, xref='paper', yref='paper', xanchor='left', yanchor='top')
    for i in range(3, 7):
        fig.add_annotation(x=0.3, y=1-0.03*(i-3), text=legend_texts[i], font=dict(color=colors[i]), showarrow=False, xref='paper', yref='paper', xanchor='left', yanchor='top')

    # Subplot titles
    fig.add_annotation(text=texts['normalized_plot_title'], x=0.5, y=0.52, xref="paper", yref="paper", showarrow=False, font=dict(size=14))
    fig.add_annotation(text=texts['distance_error_title'], x=0.15, y=0.32, xref="paper", yref="paper", showarrow=False, font=dict(size=14))
    fig.add_annotation(text=texts['course_error_title'], x=0.6, y=0.32, xref="paper", yref="paper", showarrow=False, font=dict(size=14))

    # Other text annotations
    fig.add_annotation(text=texts['normalized_plot_x_labels'][0], x=0.01, y=0.42, xref="paper", yref="paper", showarrow=False)
    fig.add_annotation(text=texts['normalized_plot_x_labels'][1], x=0.7, y=0.42, xref="paper", yref="paper", showarrow=False, xanchor='right')

    # Footer texts
    fig.add_annotation(text=texts['distance_error_footer'], x=0.15, y=-0.08, xref="paper", yref="paper", showarrow=False, font=dict(size=14))
    fig.add_annotation(text=f"{texts['course_error_footer_1']}<br>{texts['course_error_footer_2']}", x=0.6, y=-0.08, align='left', xref="paper", yref="paper", showarrow=False, font=dict(size=10))
    fig.add_annotation(text=texts['course_error_footer_3'], x=0.6, y=-0.15, xref="paper", yref="paper", showarrow=False, font=dict(size=14))

    # --- Final Output ---
    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    create_chart(json_file_path)