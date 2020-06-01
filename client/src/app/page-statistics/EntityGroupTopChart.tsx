import * as React from 'react';
import {useEffect} from 'react';
import {Chart} from 'chart.js';
import {BarColor} from './Colors';
import {EntityIdCount} from '../models';

export interface EntityGroupTopChartProps {
    title: string
    color: BarColor
    top: EntityIdCount[]
}

export function EntityGroupTopChart(props: EntityGroupTopChartProps) {
    const elementId = 'chart-entity-group-top' + props.title;
    useEffect(() => {
        const chartElement = (document.getElementById(elementId) as HTMLCanvasElement);
        if (chartElement == null) {
            return
        }

        new Chart(chartElement, {
            type: 'horizontalBar',
            data: {
                labels: props.top.map((value) => value.eid),
                datasets: [{
                    data: props.top.map((value) => value.count),
                    backgroundColor: props.color.background,
                    borderColor: props.color.border,
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

    return <canvas id={elementId} width={150} height={100}/>
}
