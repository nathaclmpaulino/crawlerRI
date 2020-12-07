import React, { useState } from 'react';

import logoImg from '../../assets/logo.png';

import api from '../../services/api';

import styles from './Main.module.scss';

const typeMethods = {
    booleano: 'booleano',
    vetorial: 'vetorial'
}

const operationsType = {
    and: 'and',
    or: 'or'
}

export default function Main() {
    const [ query, setQuery ] = useState('');
    const [ type, setType ] = useState(typeMethods.booleano);
    const [ operation, setOperation ] = useState(operationsType.and);

    async function handleQuery(e) {
        e.preventDefault();

        let params = undefined;

        if (query && type && operation) {
            params = {
                query,
                type,
                operation
            }
        }

        try {
            const response = await api.get('buscador', { params });   
            console.log(response.data[5]);
            
            alert(
                `Modelo da busca: ${type} \n` + 
                `Query: ${query} \n\n` + 
                `Busca realizada com sucesso: \n` +  
                `Numero de Documentos: ${response.data['numeroDocumentos']} \n` + 
                `5: Precisão: ${response.data[5].precisao} \n Revocação: ${response.data[5].revocacao} \n` +
                `10: Precisão: ${response.data[10].precisao} \n Revocação: ${response.data[10].revocacao} \n` +
                `25: Precisão: ${response.data[25].precisao} \n Revocação: ${response.data[25].revocacao} \n` +
                `50: Precisão: ${response.data[50].precisao} \n Revocação: ${response.data[50].revocacao} \n`);
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
                    <select name="type" onChange={(e) => setType(e.target.value)} value={type}>
                        <option value={typeMethods.booleano}>Booleano</option>
                        <option value={typeMethods.vetorial}>Vetorial</option>
                    </select>

                    {type === typeMethods.booleano && 
                        <select name="type" onChange={(e) => setOperation(e.target.value)} value={operation}>
                            <option value={operationsType.and}>Operação AND</option>
                            <option value={operationsType.vetorial}>Operação OR</option>
                        </select>
                    }

                    <button className="button" type="submit">Buscar</button>
                </form>
            </section>
        </div>
    );
}