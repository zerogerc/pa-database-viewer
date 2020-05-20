import * as React from 'react';
import './StatisticsPage.css';
import {Chart} from 'chart.js';
import {RelationTypeCountsChart} from './RelationTypeCountsChart';

export function StatisticsPage() {

    return (
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr'}}>
            <div>
                <RelationTypeCountsChart rType='CHEMICAL-GENE:increases^expression' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
            <div>
                <RelationTypeCountsChart rType='CHEMICAL-GENE:decreases^expression' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
            <div>
                <RelationTypeCountsChart rType='CHEMICAL-GENE:increases^activity' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
            <div>
                <RelationTypeCountsChart rType='CHEMICAL-GENE:decreases^activity' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
            <div>
                <RelationTypeCountsChart rType='GENE-DISEASE:therapeutic' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
            <div>
                <RelationTypeCountsChart rType='GENE-DISEASE:marker/mechanism' counts={
                    [20, 10, 5, 3, 34, 4, 23, 23, 50, 23]
                }/>
            </div>
        </div>);
}
