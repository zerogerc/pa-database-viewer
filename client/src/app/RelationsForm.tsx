import React from 'react';
import './RelationsForm.css'
import {$relationsFormStore, fetchRawExtractedRelations, relationsFormApi} from './store';
import {useStore} from 'effector-react';

export function RelationsForm() {
    const relationsFormValues = useStore($relationsFormStore);

    const entity1Component = <FormTextInput
        id="form-e1"
        label="Left entity"
        value={relationsFormValues.id1}
        onChange={(e: React.FormEvent<HTMLInputElement>) => {
            relationsFormApi.setId1(e.currentTarget.value);
        }}/>;

    const entity2Component = <FormTextInput
        id="form-e2"
        label="Right entity"
        value={relationsFormValues.id2}
        onChange={(e: React.FormEvent<HTMLInputElement>) => {
            relationsFormApi.setId2(e.currentTarget.value);
        }}/>;

    const pmidComponent = <FormTextInput
        id="form-pmid"
        label="Pmid"
        value={relationsFormValues.pmid}
        onChange={(e: React.FormEvent<HTMLInputElement>) => {
            relationsFormApi.setPmid(e.currentTarget.value);
        }}/>;

    return <div className="RelationsForm">
        <div className="RelationsForm-Inputs">
            {entity1Component}
            {entity2Component}
            {pmidComponent}
        </div>
        <button
            className="btn btn-primary"
            onClick={() => fetchRawExtractedRelations({
                id1: relationsFormValues.id1,
                id2: relationsFormValues.id2,
                pmid: relationsFormValues.pmid,
            })}>
            Make request
        </button>
    </div>;
}

interface FormTextInputProps {
    id: string,
    label: string,
    value: string,
    onChange: (e: React.FormEvent<HTMLInputElement>) => void
}

function FormTextInput(props: FormTextInputProps) {
    return <div>
        <label htmlFor={props.id}>{props.label}</label>
        <input className="form-control form-control-sm" id={props.id}
               onChange={props.onChange} value={props.value}
        />
    </div>;
}
