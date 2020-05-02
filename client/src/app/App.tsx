import React from 'react';
import './App.css';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore, $relationsFormStore, fetchRawExtractedRelations} from './store';
import {RelationsForm} from './RelationsForm';
import {RelationsTable} from './RelationsTable';
import {RelationsPagination} from './RelationsPagination';

export function App() {
    const rawExtractedRelations = useStore($rawExtractedRelationsStore);

    let paginationBlock = <></>;
    if (rawExtractedRelations.relations.length > 0) {
        paginationBlock = <RelationsPagination
            page={rawExtractedRelations.page}
            totalPages={rawExtractedRelations.totalPages}
            onPageSelected={() =>
                fetchRawExtractedRelations($relationsFormStore.getState())
            }/>;
    }

    return (
        <div className="App">
            <RelationsForm/>
            <RelationsTable relations={rawExtractedRelations.relations}/>
            {paginationBlock}
        </div>
    );
}
