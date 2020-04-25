import * as React from 'react';

export function PubmedPaperView(props: { pmid: string }) {
    return <div className="PubmedPaperView">
        <a className="btn btn-outline-info PubmedPaperView-Button"
           target="_blank"
           href={`https://www.ncbi.nlm.nih.gov/pubmed/${props.pmid}`}>
            {props.pmid}
        </a>
    </div>
}
