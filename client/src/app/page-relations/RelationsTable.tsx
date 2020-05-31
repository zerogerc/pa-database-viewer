import * as React from 'react';
import './RelationsTable.css'
import {MergedRelation} from '../models';
import {RelationPapersButton} from '../views/RelationPapersButton';
import {EntityView} from '../views/EntityView';

export function RelationsTable(props: { relations: Array<MergedRelation> }) {
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
            {props.relations.map((item: MergedRelation) => {
                return <li>
                    {createRelationsRow(
                        <EntityView entity={item.entity1}/>,
                        <EntityView entity={item.entity2}/>,
                        <span>{item.label}</span>,
                        <RelationPapersButton
                            head={item.entity1} tail={item.entity2} label={item.label} pmids={item.pmids}
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
