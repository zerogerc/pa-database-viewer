import * as React from "react";
import {ChangeEvent, useState} from "react";
import {EntitySuggestItem} from '../models';
import {SuggestionsListView} from './SuggestionsListView';
import {useStore} from 'effector-react';
import {$entitySuggestStore} from '../store';

interface InputWithSuggestionsListViewProps {
    id: string
    label: string
    entityId: string
    entityName: string
    onChange: (entityId: string, entityName: string) => void
}

export function InputWithSuggestionsListView(props: InputWithSuggestionsListViewProps) {
    const suggestStore = useStore($entitySuggestStore);
    const [isOpen, setOpen] = useState(false);


    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setOpen(true);
        props.onChange(value, '');
    };

    const handleInputFocus = () => {
        if (props.entityId != "") {
            setOpen(true);
        }
    };

    const handleSelect = (item: EntitySuggestItem) => {
        setOpen(false);
        props.onChange(item.id, item.name)
    };

    const handleClose = () => {
        setOpen(false);
    };

    const label = <label htmlFor={props.id}>{props.label}</label>;
    let suggest = <></>;
    if (isOpen && props.entityId !== "") {
        suggest = <SuggestionsListView
            suggestions={suggestStore.suggest}
            onSelect={handleSelect}
            onClose={handleClose}/>;
    }

    return (
        <div>
            {label}
            <div className="input-group">
                <input type="text" className="form-control"
                       value={props.entityId} id={props.id}
                       onChange={handleChange}
                       onFocus={handleInputFocus}
                       aria-describedby={props.id + "-addon2"}/>
                <div className="input-group-append">
                    <span className="input-group-text" id={props.id + "-addon"}>{props.entityName}</span>
                </div>
            </div>
            {suggest}
        </div>
    );
}
