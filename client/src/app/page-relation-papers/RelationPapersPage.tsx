import * as React from 'react';
import {useStore} from 'effector-react';
import {$relationPapersPageStore} from '../store';
import {PubmedPaperView} from '../views/PubmedPaperView';

export function RelationPapersPage() {
    const pageStore = useStore($relationPapersPageStore);

    return (
        <ul className="colored-list">
            {pageStore.pmids.map((pmid: string) =>
                <li><PubmedPaperView pmid={pmid}/></li>
            )}
        </ul>
    );
}
