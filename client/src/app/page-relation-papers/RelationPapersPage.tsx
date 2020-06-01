import * as React from 'react';
import './RelationPapersPage.css';
import {useStore} from 'effector-react';
import {$relationPapersPageStore, $relationPmidProbsStore} from '../store';
import {PubmedPaperView} from '../views/PubmedPaperView';
import {EntityView} from '../views/EntityView';

export function RelationPapersPage() {
    const pageStore = useStore($relationPapersPageStore);
    const pmidProbsStore = useStore($relationPmidProbsStore);

    return (
        <div>
            <div className="RelationPapersPage-Header">
                {pageStore.head ? <EntityView entity={pageStore.head}/> : <></>}
                {pageStore.label ? <span className="RelationPapersPage-Label">{pageStore.label}</span> : <></>}
                {pageStore.tail ? <EntityView entity={pageStore.tail}/> : <></>}
            </div>
            <ul className="colored-list no-bullets-list">
                {pmidProbsStore.pmidProbs.sort((a, b) => b.prob - a.prob).map(
                    (pmidProb) => <li key={pmidProb.pmid}>
                        <PubmedPaperView pmid={pmidProb.pmid} prob={pmidProb.prob}/>
                    </li>
                )}
            </ul>
        </div>
    );
}
