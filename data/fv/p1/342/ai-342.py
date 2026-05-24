import sys
import os
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=texts.get('legend_labels', [])[i],
            line=dict(color=colors[i], width=2.5)
        ))

    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Arial", color='white'),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            range=[-3.2, 3.2],
            tickvals=[-3, -2, -1, 0, 1, 2, 3],
            showgrid=True,
            gridcolor='white',
            gridwidth=1,
            griddash='dash',
            zeroline=False,
            showline=False,
            ticks='outside',
            tickcolor='white'
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[-0.05, 1.1],
            dtick=0.2,
            showgrid=True,
            gridcolor='white',
            gridwidth=1,
            griddash='dash',
            zeroline=False,
            showline=False,
            ticks='outside',
            tickcolor='white'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='black',
            bordercolor='black'
        ),
        margin=dict(l=60, r=40, t=80, b=60)
    )
    
    # Construct title and subtitle if they exist
    title_text = texts.get('title')
    subtitle_text = texts.get('subtitle')
    full_title = ""
    if title_text:
        full_title += title_text
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"
    
    if full_title:
        fig.update_layout(title=dict(text=full_title, x=0.05, xanchor='left'))

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()