import * as React from 'react';
import './PubmedPaperView.css'

export function PubmedPaperView(props: { pmid: string, prob: number }) {
    return <div className="PubmedPaperView">

        <div className={`PubmedPaperView-Prob ${getProbClassName(props.prob)}`}>
            {props.prob.toFixed(2)}
        </div>
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

function getProbClassName(prob: number): string {
    if (prob > 0.75) {
        return "score-high";
    }
    if (prob > 0.5) {
        return "score-medium";
    }
    return "score-low";
}
