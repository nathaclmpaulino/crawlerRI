import React, { useState } from 'react';

import logoImg from '../../assets/logo.png';

import api from '../../services/api';

import styles from './Main.module.scss';
 
export default function Main() {
    const [ query, setQuery ] = useState('');

    async function handleQuery(e) {
        e.preventDefault();

        let params = undefined;

        if (query) {
            params = {
                query
            }
        }

        try {
            const response = await api.get('buscador', { params });   
            alert(`Busca realizada com sucesso: ${query}`);
        } catch (err) {
            alert('Falha ao efetuar busca, favor tentar novamente');
        }

    }

    return (
        <div className={styles["container"]}>
            <section className={styles["form"]}>
                <img src={logoImg} alt="Buscador"/>

                <form onSubmit={handleQuery}>
                    <h1>Faça sua busca</h1>

                    <input 
                        placeholder="Sua Busca"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                    />
                    <button className="button" type="submit">Buscar</button>
                </form>
            </section>
        </div>
    );
}