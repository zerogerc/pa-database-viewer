import * as React from 'react';
import './App.css';
import {Route, Switch} from 'react-router';
import {RelationPapersPage} from './page-relation-papers/RelationPapersPage';
import {StatisticsPage} from './page-statistics/StatisticsPage';
import {NavBar} from './views/NavBar';
import {RelationsPage} from './page-relations/RelationsPage';
import {$collectionsStore} from './store';
import {useStore} from 'effector-react';

export function App() {
    const collectionsStore = useStore($collectionsStore);
    let app = <></>;
    if (collectionsStore.collections.length !== 0) {
        app =
            <Switch>
                <Route exact path={`${process.env.PUBLIC_URL}/`} component={RelationsPage}/>
                <Route exact path={`${process.env.PUBLIC_URL}/papers`} component={RelationPapersPage}/>
                <Route exact path={`${process.env.PUBLIC_URL}/stats`} component={StatisticsPage}/>
            </Switch>
    }
    return (
        <div>
            <NavBar/>
            <div className="App">
                {app}
            </div>
        </div>
    );
}
