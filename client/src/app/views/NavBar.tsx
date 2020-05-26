import * as React from 'react';
import {useEffect} from 'react';
import {useStore} from 'effector-react';
import {$collectionsStore, $relationsFormStore, relationsFormApi} from '../store';
import {fetchCollections} from '../api';
import './NavBar.css';

export function NavBar() {
    const collectionsStore = useStore($collectionsStore);
    const relationsFormStore = useStore($relationsFormStore);

    useEffect(() => {
        if (collectionsStore.collections.length == 0) {
            fetchCollections({});
        }
    });

    return (
        <div>
            <nav className="NavBar navbar navbar-dark bg-dark">
                <form className="form-inline">
                    {collectionsStore.collections.map((name: string) => {
                        const btnClass = relationsFormStore.collection == name ? "btn-info" : "btn-outline-info";
                        return <button
                            className={"btn btn-sm " + btnClass}
                            type="button"
                            onClick={() => relationsFormApi.setCollection(name)}>
                            {name}
                        </button>;
                    })}
                </form>
            </nav>
        </div>
    );
}
