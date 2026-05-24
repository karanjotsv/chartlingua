import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
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

    # Extract data from JSON
    data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])
    
    categories = [item['category'] for item in data]
    values = [item['value'] for item in data]

    # Create figure
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='outside',
        texttemplate='%{text:.1f}',
        textfont=dict(
            family="Arial",
            size=12,
            color=colors
        ),
        hoverinfo='none',
        cliponaxis=False
    ))

    # Construct title and subtitle
    title_text = f"<b style='font-size:24px'>{texts.get('title', '')}</b><br><span style='font-size:16px'>{texts.get('subtitle', '')}</span>"

    # Update layout
    fig.update_layout(
        plot_bgcolor='#e9f1f4',
        paper_bgcolor='white',
        showlegend=False,
        font=dict(family="Arial", size=12, color='#000000'),
        margin=dict(l=60, r=40, t=140, b=100),
        title=dict(
            text=title_text,
            y=0.97,
            x=0.01,
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            showticklabels=False, # Hide default labels, we will use annotations
            categoryorder='array',
            categoryarray=categories
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#ffffff',
            gridwidth=1,
            zeroline=False,
            showline=False,
            range=[0, max(values) * 1.1],
            tickmode='linear',
            tick0=0,
            dtick=5,
            ticksuffix=' '
        )
    )

    # Add custom colored x-axis labels using annotations
    for i, category in enumerate(categories):
        fig.add_annotation(
            x=category,
            y=0,
            yref='paper',
            yshift=-55,
            text=category,
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color=colors[i]
            ),
            textangle=-45
        )

    # Add source text annotation
    fig.add_annotation(
        text=texts.get('source', ''),
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0.99,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=11)
    )
    
    # Add horizontal separator line below title
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0,
        y0=0.88,
        x1=1,
        y1=0.88,
        line=dict(
            color="#005A9C",
            width=2,
        )
    )

    # Generate output image file path from input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Write image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()