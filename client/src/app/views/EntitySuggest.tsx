import * as React from "react";
import {ChangeEvent, useEffect, useRef, useState} from "react";
import {EntitySuggestItem} from '../models';
import './EntitySuggest.css';
import {useStore} from 'effector-react';
import {$entitySuggestStore} from '../store';
import {fetchEntitySuggest} from '../api';

interface EntitySuggestProps {
    suggestions: EntitySuggestItem[]
    onSelect: (arg: EntitySuggestItem) => void
    onClose: () => void
}

export function EntitySuggestListView(props: EntitySuggestProps) {
    const ref = useRef<HTMLDivElement>(null);

    const outsideClickHandler = (event: MouseEvent) => {
        if (event.target instanceof Element && ref.current && !ref.current.contains(event.target)) {
            props.onClose();
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", outsideClickHandler);
        return () => {
            document.removeEventListener("mousedown", outsideClickHandler);
        };
    }, []);

    return <div ref={ref} className="list-group EntitySuggest-List">
        {props.suggestions
            .map((suggestion: EntitySuggestItem, index) =>
                <a key={index}
                   onClick={() => props.onSelect(suggestion)}
                   href="#"
                   className="list-group-item list-group-item-action"
                >
                    {suggestion.id} ({suggestion.name})
                </a>
            )
        }
    </div>;
}

interface InputWithSuggestionProps {
    id: string
    label: string
    value: string
    suggestions: EntitySuggestItem[]
    onChange: (query: string) => void
}

export function InputWithSuggestion(props: InputWithSuggestionProps) {
    const [isCompleted, setCompleted] = useState(false);
    const [isOpen, setOpen] = useState(false);

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setCompleted(false);
        setOpen(true);
        props.onChange(value);
    };

    const handleInputFocus = () => {
        if (props.value != "") {
            setOpen(true);
        }
    };

    const handleSelect = (item: EntitySuggestItem) => {
        setOpen(false);
        setCompleted(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    const label = <label htmlFor={props.id}>{props.label}</label>;
    const input = <input className="form-control form-control-sm" value={props.value} id={props.id}
                         onChange={handleChange}
                         onFocus={handleInputFocus}/>;
    let suggest = <></>;
    if (isOpen && props.value !== "" && !isCompleted) {
        suggest = <EntitySuggestListView
            suggestions={props.suggestions}
            onSelect={handleSelect}
            onClose={handleClose}/>;
    }

    return (
        <div>
            {label}
            {input}
            {suggest}
        </div>
    );
}

export function SuggestView() {
    const suggestStore = useStore($entitySuggestStore);
    const [text, setText] = useState('');

    const handleChange = (query: string) => {
        fetchEntitySuggest({query: query});
        setText(query);
    };

    return (
        <InputWithSuggestion
            id={'entity-suggest'}
            label="Entity Suggest"
            value={text}
            suggestions={suggestStore.suggest}
            onChange={handleChange}
        />
    );

}
