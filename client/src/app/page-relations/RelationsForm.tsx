import * as React from 'react';
import './RelationsForm.css'
import {$relationsFormStore, relationsFormApi} from '../store';
import {useStore} from 'effector-react';
import {fetchRelationsUsingFormValues} from '../utils';
import {InputWithSuggestionsListView} from '../views/InputWithSuggestionsListView';
import {fetchEntitySuggest} from '../api';

export function RelationsForm() {
    const relationsFormValues = useStore($relationsFormStore);

    const entity1Component = <InputWithSuggestionsListView
        id="form-e1"
        label="Left entity"
        entityId={relationsFormValues.id1}
        entityName={relationsFormValues.name1}
        onChange={(eId: string, eName: string) => {
            relationsFormApi.setId1(eId);
            relationsFormApi.setName1(eName);
            fetchEntitySuggest({collection: relationsFormValues.collection, query: eId});
        }}/>;

    const entity2Component = <InputWithSuggestionsListView
        id="form-e2"
        label="Right entity"
        entityId={relationsFormValues.id2}
        entityName={relationsFormValues.name2}
        onChange={(eId: string, eName: string) => {
            relationsFormApi.setId2(eId);
            relationsFormApi.setName2(eName);
            fetchEntitySuggest({collection: relationsFormValues.collection, query: eId});
        }}/>;

    const pmidComponent = <FormTextInput
        id="form-pmid"
        label="Pmid"
        value={relationsFormValues.pmid}
        onChange={(e: React.FormEvent<HTMLInputElement>) => {
            relationsFormApi.setPmid(e.currentTarget.value);
        }}/>;

    const onlyNovelComponent =
        <div className="form-check">
            <input
                id="form-novel"
                className="form-check-input" type="checkbox"
                checked={relationsFormValues.onlyNovel}
                onChange={(e: React.FormEvent<HTMLInputElement>) => {
                    relationsFormApi.setOnlyNovel(e.currentTarget.checked)
                }}/>
            <label htmlFor="form-novel" className="form-check-label">Only novel</label>
        </div>;

    return (
        <div>
            <div className="RelationsForm">
                <div className="RelationsForm-Inputs">
                    {entity1Component}
                    {entity2Component}
                    {pmidComponent}
                    {onlyNovelComponent}
                </div>
                <button
                    className="btn btn-primary"
                    onClick={() => {
                        fetchRelationsUsingFormValues();
                        relationsFormApi.setDefaultPage();
                    }}>
                    Make request
                </button>
            </div>
        </div>);
}

interface FormTextInputProps {
    id: string,
    label: string,
    value: string,
    onChange: (e: React.FormEvent<HTMLInputElement>) => void
}

function FormTextInput(props: FormTextInputProps) {
    return <div className="form-group">
        <label htmlFor={props.id}>{props.label}</label>
        <input className="form-control" id={props.id}
               onChange={props.onChange} value={props.value}
        />
    </div>;
}
