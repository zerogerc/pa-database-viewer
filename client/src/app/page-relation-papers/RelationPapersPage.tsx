import * as React from 'react';
import {useEffect} from 'react';
import {useStore} from 'effector-react';
import {$relationPmidProbsStore, clearRelationPmidProbsStore} from '../store';
import {PubmedPaperView} from '../views/PubmedPaperView';

export function RelationPapersPage() {
    const pmidProbsStore = useStore($relationPmidProbsStore);

    useEffect(() => {
        return () => {
            clearRelationPmidProbsStore();
        }
    }, [pmidProbsStore.pmidProbs]);

    return (
        <ul className="colored-list no-bullets-list">
            {pmidProbsStore.pmidProbs.map((pmidProb) =>
                <li><PubmedPaperView pmid={pmidProb.pmid}/></li>
            )}
        </ul>
    );
}
