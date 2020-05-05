import * as React from 'react';

export function PubmedPaperView(props: { pmid: string }) {
    return <div className="PubmedPaperView">
        <div className="PubmedPaperView-Pmid">
            {props.pmid}
        </div>
        <div className="PubmedPaperView-Links">
            <a target="_blank"
               href={"https://www.ncbi.nlm.nih.gov/research/pubtator/index.html?view=docsum&query=" + props.pmid}>
                [Pubtator]
            </a>
            <a target="_blank" href={"https://www.ncbi.nlm.nih.gov/pubmed/" + props.pmid}>[Pubmed]</a>
        </div>
    </div>
}
