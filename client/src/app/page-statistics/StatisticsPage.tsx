import * as React from 'react';
import {useEffect} from 'react';
import {RelationTypeCountsChart} from './RelationTypeCountsChart';
import {$relationsFormStore, $statsStore} from '../store';
import {fetchStats} from '../api';
import {useStore} from 'effector-react';
import {EntityGroupCountsChart} from './EntityGroupCountsChart';
import {EntityGroupTopChart} from './EntityGroupTopChart';
import {CHEMICAL_COLOR, DISEASE_COLOR, GENE_COLOR} from './Colors';

export function StatisticsPage() {
    const statsStore = useStore($statsStore);
    const relationsFormStore = useStore($relationsFormStore);

    useEffect(() => {
        fetchStats({collection: relationsFormStore.collection});
    }, [relationsFormStore.collection]);

    return (
        <div>
            <h4>Total Relations: {statsStore.stats.totalRelations} | Total
                Entities: {statsStore.stats.totalEntities}</h4>
            <hr/>

            <h3>Entity Group Statistics</h3>
            <hr/>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr'}}>
                <div>
                    <EntityGroupCountsChart
                        title='Relations Count'
                        chemicals={statsStore.stats.chemicals.relations}
                        genes={statsStore.stats.genes.relations}
                        diseases={statsStore.stats.diseases.relations}/>
                </div>
                <div>
                    <EntityGroupCountsChart
                        title='Unique Entity Identifiers'
                        chemicals={statsStore.stats.chemicals.total}
                        genes={statsStore.stats.genes.total}
                        diseases={statsStore.stats.diseases.total}/>
                </div>
            </div>

            <h3>Entity Identifiers with Highest Number of Relations</h3>
            <hr/>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr'}}>
                <div>
                    <EntityGroupTopChart
                        title='Chemicals' color={CHEMICAL_COLOR}
                        top={statsStore.stats.chemicals.top}/>
                </div>
                <div>
                    <EntityGroupTopChart
                        title='Genes' color={GENE_COLOR}
                        top={statsStore.stats.genes.top}/>
                </div>
                <div>
                    <EntityGroupTopChart
                        title='Diseases' color={DISEASE_COLOR}
                        top={statsStore.stats.diseases.top}/>
                </div>
            </div>

            <h3>Relation Counts Distribution by Relation Type</h3>
            <hr/>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr'}}>
                {statsStore.stats.rTypeCounts.map((rTypeCounts) =>
                    <div>
                        <RelationTypeCountsChart rType={rTypeCounts.rType} counts={rTypeCounts.counts}/>
                    </div>
                )}
            </div>
        </div>);
}
