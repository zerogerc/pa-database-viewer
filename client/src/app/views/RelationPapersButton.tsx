import * as React from 'react';
import {Link} from 'react-router-dom';
import {fetchRelationPmidProbs} from '../api';

export function RelationPapersButton(props: { id1: string, id2: string, label: string, pmids: string[] }) {
    return <div>
        <Link className="btn btn-outline-info"
              to={`/papers`}
              onClick={() => {
                  fetchRelationPmidProbs({
                      id1: props.id1,
                      id2: props.id2,
                      label: props.label,
                      pmids: props.pmids
                  })
              }}>
            {props.pmids.length} {props.pmids.length == 1 ? 'paper' : 'papers'}
        </Link>
    </div>
}
