import React from 'react';
import './RelationsTable.css'
import {RawExtractedRelation} from './models';
import {RelationPapersButton} from './views/RelationPapersButton';
import {EntityView} from './EntityViewV';

export function RelationsTable(props: { relations: Array<RawExtractedRelation> }) {
    return <div>
        {createRelationsRow(
            <span>Entity 1</span>,
            <span>Entity 2</span>,
            <span>Label</span>,
            <span>Pmid</span>,
            <span>Prob</span>,
            "RelationsTable-Row-Header"
        )}
        <ul className="RelationsTable-List colored-list">
            {props.relations.map((item: RawExtractedRelation) => {
                return <li>
                    {createRelationsRow(
                        <EntityView entity={item.head}/>,
                        <EntityView entity={item.tail}/>,
                        <span>{item.label}</span>,
                        <RelationPapersButton
                            head={item.head} tail={item.tail} label={item.label} pmids={item.pmids}
                        />,
                        <span>{item.prob.toFixed(4)}</span>
                    )}
                </li>
            })}
        </ul>
    </div>;
}

function createRelationsRow(
    e1: React.ReactElement, e2: React.ReactElement,
    label: React.ReactElement, pmid: React.ReactElement, prob: React.ReactElement,
    className: string = ''): React.ReactElement {
    return <div className={"RelationsTable-Row " + className}>
        {wrapCell(e1)}
        {wrapCell(e2)}
        {wrapCell(label)}
        {wrapCell(pmid)}
        {wrapCell(prob)}
    </div>
}

function wrapCell(el: React.ReactElement) {
    return <div className="RelationsTable-Cell">{el}</div>
}
