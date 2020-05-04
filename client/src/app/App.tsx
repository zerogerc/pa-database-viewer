import React from 'react';
import './App.css';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore, $relationsFormStore, fetchRawExtractedRelations} from './store';
import {RelationsForm} from './RelationsForm';
import {RelationsTable} from './RelationsTable';
import {RelationsPagination} from './RelationsPagination';
import {Route, Switch} from 'react-router';

export function App() {
    return (
        <div className="App">
            <Switch>
                <Route exact path="/" component={RelationsPage}/>
                <Route exact path="/papers" component={RelationPapersPage}/>
            </Switch>
        </div>
    );
}

export function RelationsPage() {
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
        <div>
            <RelationsForm/>
            <RelationsTable relations={rawExtractedRelations.relations}/>
            {paginationBlock}
        </div>
    );
}

export function RelationPapersPage() {
    return (
        <h1>This is a page for papers of single relation</h1>
    );
}
