import * as React from 'react';
import {Entity} from '../models';

export function EntityView(props: { entity: Entity }) {
    return <span className={props.entity.group.toLowerCase()}>{props.entity.name}({props.entity.id})</span>;
}
