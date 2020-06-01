import * as React from 'react';
import {Link} from 'react-router-dom';
import {fetchRelationPmidProbs} from '../api';
import {relationPapersPageStoreApi} from '../store';
import {Entity} from '../models';

export function RelationPapersButton(props: { head: Entity, tail: Entity, label: string, pmids: string[] }) {
    return <div>
        <Link className="btn btn-outline-info"
              to={`/papers`}
              onClick={() => {
                  relationPapersPageStoreApi.setStore({
                      head: props.head,
                      tail: props.tail,
                      label: props.label
                  });
                  fetchRelationPmidProbs({
                      id1: props.head.id,
                      id2: props.tail.id,
                      label: props.label,
                      pmids: props.pmids
                  })
              }}>
            {props.pmids.length} {props.pmids.length === 1 ? 'paper' : 'papers'}
        </Link>
    </div>
}
