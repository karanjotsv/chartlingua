import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    image_filename_base = os.path.splitext(os.path.basename(json_path))[0]
    
    chart_data = chart_config.get('chart_data', {})
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', {})

    fig = go.Figure()

    # --- Pie Chart ---
    pie_data = chart_data.get('pie', {})
    if pie_data:
        fig.add_trace(go.Pie(
            labels=pie_data.get('labels', []),
            values=pie_data.get('values', []),
            marker=dict(colors=colors.get('pie', [])),
            domain=dict(x=[0, 0.6], y=[0, 1]),
            texttemplate="%{label}<br>%{value}%",
            textposition='auto',
            textfont=dict(family="Arial", size=12),
            insidetextorientation='horizontal',
            sort=False,
            direction='clockwise',
            rotation=115,
            showlegend=False
        ))

    # --- Bar Chart (Breakout) ---
    bar_data = chart_data.get('bar', {})
    bar_labels = bar_data.get('labels', [])
    bar_values = bar_data.get('values', [])
    bar_colors = colors.get('bar', [])
    
    if bar_labels:
        # Add bar traces from bottom to top
        for i in range(len(bar_labels) - 1, -1, -1):
            fig.add_trace(go.Bar(
                x=[''], 
                y=[bar_values[i]], 
                name=bar_labels[i],
                marker_color=bar_colors[i],
                showlegend=False,
                hoverinfo='none'
            ))

        # Add annotations for bar labels
        y_cumulative = 0
        for i in range(len(bar_labels) - 1, -1, -1):
            label = bar_labels[i]
            value = bar_values[i]
            y_mid = y_cumulative + value / 2.0
            
            # Position for 0-value items
            if value == 0:
                y_mid = y_cumulative

            # Special case for 'IND' label to be outside
            if label == "IND":
                 fig.add_annotation(
                    xref="paper", yref="y1",
                    x=0.86, y=y_cumulative,
                    text=f"{label}<br>{value}%",
                    showarrow=False,
                    xanchor='left',
                    yanchor='middle',
                    align='left',
                    font=dict(family="Arial", size=12)
                )
            else:
                # Other labels inside the bar segments
                fig.add_annotation(
                    xref="x1", yref="y1",
                    x=0, y=y_mid,
                    text=f"{label}<br>{value}%",
                    showarrow=False,
                    xanchor='center',
                    yanchor='middle',
                    font=dict(family="Arial", size=12, color='white' if label != "PNDC" else "black")
                )
            
            y_cumulative += value
            
    # --- Layout and Styling ---
    full_title = ""
    if texts.get("title"):
        full_title += f"<b>{texts['title']}</b>"
    if texts.get("subtitle"):
        full_title += f"<br>{texts['subtitle']}"
    
    total_bar_value = sum(bar_values) if bar_values else 1

    fig.update_layout(
        title_text=full_title,
        title_x=0.5,
        font=dict(family="Arial"),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=120, t=40, b=20),
        barmode='stack',
        xaxis1=dict(
            domain=[0.7, 0.85],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.5, 0.5]
        ),
        yaxis1=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, total_bar_value]
        ),
        shapes=[
            dict(type="line", xref="paper", yref="paper",
                 x0=0.55, y0=0.6, x1=0.7, y1=0.9,
                 line=dict(color="black", width=1)),
            dict(type="line", xref="paper", yref="paper",
                 x0=0.55, y0=0.4, x1=0.7, y1=0.1,
                 line=dict(color="black", width=1))
        ]
    )

    # --- Output ---
    output_filename = f"{image_filename_base}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()