import * as React from 'react';
import './App.css';
import {Route, Switch} from 'react-router';
import {RelationPapersPage} from './page-relation-papers/RelationPapersPage';
import {StatisticsPage} from './page-statistics/StatisticsPage';
import {NavBar} from './views/NavBar';
import {RelationsPage} from './page-relations/RelationsPage';

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
