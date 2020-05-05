import {fetchRawExtractedRelations} from './api';
import {$relationsFormStore} from './store';

export function fetchRelationsUsingFormValues() {
    const formState = $relationsFormStore.getState();

    return fetchRawExtractedRelations({
        id1: formState.id1,
        id2: formState.id2,
        pmid: formState.pmid,
        onlyNovel: formState.onlyNovel ? 1 : 0,
        page: formState.page,
    });
}
