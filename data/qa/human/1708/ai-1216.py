import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Load data from JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    # Extract data and texts
    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']
    
    # Data needs to be reversed for horizontal bar chart display order
    categories_reversed = chart_data['categories'][::-1]
    
    # Initialize figure
    fig = go.Figure()

    # Add traces for each series
    for i, series in enumerate(chart_data['series']):
        series_data_reversed = series['data'][::-1]
        
        # Generate text labels, hiding for values less than 5
        text_labels = [str(val) if val >= 5 else '' for val in series_data_reversed]
        
        # Determine if the series should be shown in the legend
        show_legend = series['name'] != "Not shown"
        
        fig.add_trace(go.Bar(
            y=categories_reversed,
            x=series_data_reversed,
            name=series['name'],
            orientation='h',
            marker=dict(
                color=colors[i],
                line=dict(color='white', width=1)
            ),
            text=text_labels,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(family="Arial", size=14, color='black'),
            hoverinfo='none',
            showlegend=show_legend
        ))

    # Combine title and subtitle
    title_text = (
        f"<b style='font-size: 22px;'>{texts['title']}</b><br>"
        f"<span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"
    )

    # Combine source and credit
    source_text = (
        f"{texts['source']}<br>"
        f"<b>{texts['credit']}</b>"
    )
    
    # Update layout
    fig.update_layout(
        barmode='stack',
        title=dict(
            text=title_text,
            y=0.98,
            x=0.01,
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, 100]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            tickfont=dict(size=14, family="Arial"),
            autorange=False, # Ensure reversed order is maintained
            range=[-0.5, len(categories_reversed) - 0.5]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            font=dict(family="Arial", size=14),
            traceorder="normal"
        ),
        margin=dict(l=200, r=30, t=130, b=80),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial"),
        height=600,
        width=700
    )

    # Add source and credit annotation
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=12, color='#555555')
    )

    # Generate output PNG file path
    output_filename = json_path.stem + ".png"
    
    # Save the figure
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()