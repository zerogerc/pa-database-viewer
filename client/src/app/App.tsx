import React from 'react';
import './App.css';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore} from './store';
import {RelationsForm} from './RelationsForm';

export function App() {
    const rawExtractedRelations = useStore($rawExtractedRelationsStore);

    return (
        <div className="App">
            <RelationsForm/>
            <ul>
                {rawExtractedRelations.map((item, idx) =>
                    <li key={idx}>{item.id1} {item.id2} {item.label} {item.pmid}</li>)
                }
            </ul>
        </div>
    );
}
