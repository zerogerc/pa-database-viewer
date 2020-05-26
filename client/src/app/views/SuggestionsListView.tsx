import * as React from "react";
import {useEffect, useRef} from "react";
import {EntitySuggestItem} from '../models';
import './SuggestionsListView.css';

interface SuggestionsListViewProps {
    suggestions: EntitySuggestItem[]
    onSelect: (arg: EntitySuggestItem) => void
    onClose: () => void
}

export function SuggestionsListView(props: SuggestionsListViewProps) {
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

    return <div ref={ref} className="list-group SuggestionsListView">
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
