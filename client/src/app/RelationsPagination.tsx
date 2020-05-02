import * as React from 'react';
import {useEffect} from 'react';
import {relationsFormApi} from './store';

export function RelationsPagination(props: { page: number, totalPages: number, onPageSelected: () => void }): React.ReactElement {

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [props.page]);

    const selectPage = (page: number) => {
        if (page == props.page) {
            return;
        }
        relationsFormApi.setPage(page);
        props.onPageSelected();
    };

    let pages = [];
    let ellipsisPages = 5;
    let startPage = Math.max(1, props.page - ellipsisPages);
    let endPage = Math.min(props.totalPages, props.page + ellipsisPages);
    let ellipsisStart = startPage > 1;
    let ellipsisEnd = endPage < props.totalPages;

    if (ellipsisStart) {
        pages.push(<li key={1} className={`page-item`}>
            <span className="page-link" onClick={(e: any) => selectPage(1)}>1</span>
        </li>);
        pages.push(<li key={2} className={`page-item`}><span className="page-link">…</span></li>);
        startPage++;
    }

    for (let number = startPage; number <= endPage; number++) {
        const activeClassName = number == props.page ? " active" : "";
        const _number = number;
        pages.push(<li key={number} className={`page-item ${activeClassName}`}>
            <span className="page-link" onClick={() => selectPage(_number)}>{number}</span>
        </li>);
    }

    if (ellipsisEnd) {
        pages.pop();
        pages.push(<li key={props.totalPages - 1} className={`page-item`}><span
            className="page-link">…</span></li>);
        pages.push(<li key={props.totalPages} className={`page-item`}>
            <span className="page-link" onClick={(e: any) => selectPage(props.totalPages)}>{props.totalPages}</span>
        </li>);
    }

    return <ul className="pagination">
        {pages}
    </ul>;
}
