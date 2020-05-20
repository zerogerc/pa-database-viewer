import * as React from 'react';
import {useEffect} from 'react';
import {Chart} from 'chart.js';

export interface RelationTypeCountsChartProps {
    rType: string,
    counts: number[],
    color?: string,
}

export function RelationTypeCountsChart(props: RelationTypeCountsChartProps) {
    const elementId = 'chart-relation-type-counts' + props.rType;
    const color = props.color ? props.color : 'rgba(54, 162, 235, 0.2)';
    useEffect(() => {
        const chartElement = (document.getElementById(elementId) as HTMLCanvasElement);
        if (chartElement == null) {
            return
        }

        new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: createLabels(props.counts),
                datasets: [{
                    label: props.rType,
                    data: props.counts,
                    backgroundColor: color,
                    borderWidth: 0,
                    barPercentage: 1.0,
                    categoryPercentage: 1.0
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                            stepSize: 0.2,
                        }
                    }]
                }
            }
        });
    });

    return <canvas id={elementId} width={100} height={100}/>
}

function createLabels(counts: number[]): string[] {
    return counts.map((_, index: number) => ((index + 1) / counts.length).toFixed(2))
}
