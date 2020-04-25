import React from 'react';
import './RelationsTable.css'
import {RawExtractedRelation} from './models';

export function RelationsTable(props: { relations: Array<RawExtractedRelation> }) {
    return <div>
        {createRelationsRow(
            <span>Entity 1</span>,
            <span>Entity 2</span>,
            <span>Label</span>,
            <span>Pmid</span>,
            "RelationsTable-Row-Header"
        )}
        <ul className="RelationsTable-List colored-list">
            {props.relations.map((item: RawExtractedRelation) =>
                <li>
                    {createRelationsRow(
                        <span>{item.id1}</span>,
                        <span>{item.id2}</span>,
                        <span>{item.label}</span>,
                        <span>{item.pmid}</span>
                    )}
                </li>
            )}
        </ul>
    </div>;
}

function createRelationsRow(
    id1: React.ReactElement, id2: React.ReactElement, label: React.ReactElement, pmids: React.ReactElement,
    className: string = ''): React.ReactElement {
    return <div className={"RelationsTable-Row " + className}>
        {id1}
        {id2}
        {label}
        {pmids}
    </div>
}
