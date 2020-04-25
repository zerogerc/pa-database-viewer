import React from 'react';
import {$relationsFormStore, fetchRawExtractedRelations, relationsFormApi} from './store';
import {useStore} from 'effector-react';

export function RelationsForm() {
    const relationsFormValues = useStore($relationsFormStore);

    const entity1Component =
        <div>
            <label htmlFor="form-id1">Entity 1</label>
            <input className="form-control form-control-sm"
                   id="form-id1"
                   onChange={(e: React.FormEvent<HTMLInputElement>) => {
                       relationsFormApi.setId1(e.currentTarget.value);
                   }}
                   value={relationsFormValues.id1}
            />
        </div>;

    const entity2Component =
        <div>
            <label htmlFor="form-id2">Entity 2</label>
            <input className="form-control form-control-sm"
                   id="form-id2"
                   onChange={(e: React.FormEvent<HTMLInputElement>) => {
                       relationsFormApi.setId2(e.currentTarget.value);
                   }}
                   value={relationsFormValues.id2}
            />
        </div>;

    return <div>
        <div style={{marginBottom: "1em", marginTop: "1em"}}>
            {entity1Component}
            {entity2Component}
        </div>
        <button
            onClick={() => fetchRawExtractedRelations({id1: relationsFormValues.id1, id2: relationsFormValues.id2})}>
            Make request
        </button>
    </div>;
}

