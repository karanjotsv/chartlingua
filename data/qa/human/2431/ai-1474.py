import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Generates a Plotly chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data['series']):
        text_labels = [f"{val:.1f}%" for val in series['data']]
        # The last data point in the original image does not have a label
        text_labels[-1] = ''

        fig.add_trace(go.Scatter(
            x=chart_data['categories'],
            y=series['data'],
            name=series.get('name', ''),
            mode='lines+markers+text',
            line=dict(color=colors[i % len(colors)], width=2.5),
            marker=dict(color=colors[i % len(colors)], size=8),
            text=text_labels,
            textposition=series['text_positions'],
            textfont=dict(
                family="Arial",
                size=12,
                color='black'
            )
        ))

    # Combine source and note for the annotation
    source_note_text = ""
    if texts.get('source'):
        source_note_text += texts['source']
    if texts.get('note'):
        if source_note_text:
            source_note_text += "<br>"
        source_note_text += texts['note']

    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=12),
            fixedrange=True
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[10, 13.6],
            tickvals=[10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5],
            ticktext=["10%", "10.5%", "11%", "11.5%", "12%", "12.5%", "13%", "13.5%"],
            gridcolor='#E5E5E5',
            zeroline=False,
            fixedrange=True
        ),
        showlegend=False,
        margin=dict(l=80, r=40, t=50, b=100),
        annotations=[
            dict(
                showarrow=False,
                text=source_note_text,
                xref="paper",
                yref="paper",
                x=1.0,
                y=-0.2,
                xanchor='right',
                yanchor='top',
                align='right',
                font=dict(size=12)
            )
        ]
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Added a main guard and function definition for better structure,
    # but the core logic remains a simple, straight script as requested.
    main()