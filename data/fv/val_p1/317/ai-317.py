import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'")
        sys.exit(1)

    data = chart_data['chart_data'][0]
    texts = chart_data['texts']
    colors = chart_data['colors']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data['x_labels'],
        y=data['y_values'],
        marker_color=colors,
        text=[f"{y}%" for y in data['y_values']],
        textposition='outside',
        hoverinfo='none',
        cliponaxis=False 
    ))

    fig.update_layout(
        title_text=texts['title'],
        title_x=0.5,
        title_font_family="Arial",
        title_font_size=20,
        font=dict(
            family="Arial",
            size=12
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            title_font_size=14,
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
            range=[0, 105],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont_size=12
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(t=100, b=150, l=100, r=40),
        annotations=[
            dict(
                text=texts['source_note'],
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.25,
                xanchor='left',
                yanchor='top',
                align='left',
                font=dict(size=11)
            )
        ]
    )

    fig.update_traces(
        textfont=dict(
            family='Arial',
            size=14,
            color='black'
        )
    )

    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    output_image_path = f"{base_filename}.png"
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()