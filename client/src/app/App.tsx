import React from 'react';
import './App.css';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore} from './store';
import {RelationsForm} from './RelationsForm';
import {RelationsTable} from './RelationsTable';

export function App() {
    const rawExtractedRelations = useStore($rawExtractedRelationsStore);

    return (
        <div className="App">
            <RelationsForm/>
            <RelationsTable relations={rawExtractedRelations.relations}/>
        </div>
    );
}
