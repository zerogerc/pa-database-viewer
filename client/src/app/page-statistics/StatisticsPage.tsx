import * as React from 'react';
import {useEffect} from 'react';
import './StatisticsPage.css';
import {Chart} from 'chart.js';
import {RelationTypeCountsChart} from './RelationTypeCountsChart';
import {$statsStore} from '../store';
import {fetchStats} from '../api';
import {useStore} from 'effector-react';

export function StatisticsPage() {
    const statsStore = useStore($statsStore);
    useEffect(() => {
        if (statsStore.rTypeCounts.length == 0) {
            fetchStats({});
        }
    });

    return (
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr'}}>
            {statsStore.rTypeCounts.map((rTypeCounts) =>
                <div>
                    <RelationTypeCountsChart rType={rTypeCounts.rType} counts={rTypeCounts.counts}/>
                </div>
            )}
        </div>);
}
