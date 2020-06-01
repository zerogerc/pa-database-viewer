import * as React from 'react';
import {useEffect} from 'react';
import {Chart} from 'chart.js';
import {CHEMICAL_COLOR, DISEASE_COLOR, GENE_COLOR} from './Colors';

export interface EntityGroupCountsChartProps {
    title: string
    chemicals: number
    genes: number
    diseases: number
}

export function EntityGroupCountsChart(props: EntityGroupCountsChartProps) {
    const elementId = 'chart-entity-group-counts' + props.title;
    useEffect(() => {
        const chartElement = (document.getElementById(elementId) as HTMLCanvasElement);
        if (chartElement == null) {
            return
        }

        new Chart(chartElement, {
            type: 'horizontalBar',
            data: {
                labels: ['CHEMICAL', 'GENE', 'DISEASE'],
                datasets: [{
                    data: [props.chemicals, props.genes, props.diseases],
                    backgroundColor: [
                        CHEMICAL_COLOR.background,
                        GENE_COLOR.background,
                        DISEASE_COLOR.background,
                    ],
                    borderColor: [
                        CHEMICAL_COLOR.border,
                        GENE_COLOR.border,
                        DISEASE_COLOR.border,
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                title: {
                    display: true,
                    text: props.title
                },
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                        }
                    }]
                }
            }
        });
    });

    return <canvas id={elementId} width={200} height={100}/>
}
