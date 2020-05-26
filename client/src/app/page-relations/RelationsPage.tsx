import * as React from 'react';
import {useStore} from 'effector-react';
import {$rawExtractedRelationsStore} from '../store';
import {RelationsForm} from './RelationsForm';
import {RelationsTable} from './RelationsTable';
import {RelationsPagination} from './RelationsPagination';
import {fetchRelationsUsingFormValues} from '../utils';

export function RelationsPage() {
    const rawExtractedRelations = useStore($rawExtractedRelationsStore);

    let paginationBlock = <></>;
    if (rawExtractedRelations.relations.length > 0) {
        paginationBlock = <RelationsPagination
            page={rawExtractedRelations.page}
            totalPages={rawExtractedRelations.totalPages}
            onPageSelected={() => fetchRelationsUsingFormValues()}/>;
    }

    return (
        <div>
            <RelationsForm/>
            <RelationsTable relations={rawExtractedRelations.relations}/>
            {paginationBlock}
        </div>
    );
}
