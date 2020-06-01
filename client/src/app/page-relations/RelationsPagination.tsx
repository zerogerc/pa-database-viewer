import * as React from 'react';
import {relationsFormApi} from '../store';

export function RelationsPagination(props: { page: number, totalPages: number, onPageSelected: () => void }): React.ReactElement {

    const selectPage = (page: number) => {
        if (page === props.page) {
            return;
        }
        relationsFormApi.setPage(page);
        props.onPageSelected();
    };

    let pages = [];
    let ellipsisPages = 5;
    let startPage = Math.max(0, props.page - ellipsisPages);
    let endPage = Math.min(props.totalPages - 1, props.page + ellipsisPages);
    let ellipsisStart = startPage > 0;
    let ellipsisEnd = endPage < props.totalPages - 1;

    if (ellipsisStart) {
        pages.push(<PageLink key="0" text="1" onClick={() => selectPage(0)}/>);
        pages.push(<PageLink key="ellipsis-start" text="…"/>);
        startPage++;
    }

    for (let number = startPage; number <= endPage; number++) {
        const activeClassName = number === props.page ? " active" : "";
        const _number = number;
        pages.push(<PageLink key={`${number}`} text={`${number + 1}`} className={activeClassName}
                             onClick={() => selectPage(_number)}/>);
    }

    if (ellipsisEnd) {
        pages.pop();
        pages.push(<PageLink key="ellipsis-end" text="…"/>);
        pages.push(<PageLink key={`${props.totalPages - 1}`} text={`${props.totalPages}`}
                             onClick={() => selectPage(props.totalPages - 1)}/>);
    }

    return (
        <ul className="pagination">
            {pages}
        </ul>);
}

export function PageLink(props: { text: string, className?: string, onClick?: () => void }) {
    const pageClassName = "page-item" + (props.className != null ? props.className : "");
    return (<li className={pageClassName}>
        <span className="page-link" onClick={props.onClick}>{props.text}</span>
    </li>);
}
