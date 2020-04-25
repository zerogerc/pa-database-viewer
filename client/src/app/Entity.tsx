import * as React from 'react';

export function Entity(props: { name: string, id: string, group: string }) {
    return <span className={props.group.toLowerCase()}>{props.name}({props.id})</span>;
}
