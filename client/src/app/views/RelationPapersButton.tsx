import * as React from 'react';
import {Link} from 'react-router-dom';
import {relationPapersPageStoreApi} from '../store';

export function RelationPapersButton(props: { pmids: string[] }) {
    return <div>
        <Link className="btn btn-outline-info"
              to={`/papers`}
              onClick={() => {
                  relationPapersPageStoreApi.setPmids(props.pmids)
              }}>
            {props.pmids.length} {props.pmids.length == 1 ? 'paper' : 'papers'}
        </Link>
    </div>
}
