import * as React from 'react';
import './App.css';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore} from './store';
import {RelationsForm} from './RelationsForm';
import {RelationsTable} from './RelationsTable';
import {RelationsPagination} from './RelationsPagination';
import {Route, Switch} from 'react-router';
import {RelationPapersPage} from './page-relation-papers/RelationPapersPage';
import {fetchRelationsUsingFormValues} from './utils';
import {StatisticsPage} from './page-statistics/StatisticsPage';
import {NavBar} from './views/NavBar';

export function App() {
    return (
        <div>
            <NavBar/>
            <div className="App">
                <Switch>
                    <Route exact path="/" component={RelationsPage}/>
                    <Route exact path="/papers" component={RelationPapersPage}/>
                    <Route exact path="/stats" component={StatisticsPage}/>
                </Switch>
            </div>
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
            onPageSelected={() => fetchRelationsUsingFormValues()}/>;
    }

    return (
        <div>
            <RelationsForm/>
            <RelationsTable relations={rawExtractedRelations.relations}/>
            {paginationBlock}
        </div>
    );
}
