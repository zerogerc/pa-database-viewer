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

    useEffect(() => {
        const outsideClickHandler = (event: MouseEvent) => {
            if (event.target instanceof Element && ref.current && !ref.current.contains(event.target)) {
                props.onClose();
            }
        };

        document.addEventListener("mousedown", outsideClickHandler);
        return () => {
            document.removeEventListener("mousedown", outsideClickHandler);
        };
    }, [props]);

    return <div ref={ref} className="list-group SuggestionsListView">
        {props.suggestions
            .map((suggestion: EntitySuggestItem, index) =>
                <button key={index}
                   onClick={() => props.onSelect(suggestion)}
                   className="list-group-item list-group-item-action"
                >
                    {suggestion.id} ({suggestion.name})
                </button>
            )
        }
    </div>;
}
