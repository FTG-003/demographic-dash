# Contributing

## Italian Demographic Observatory

### Principi

1. **Semplicità architetturale** — nessun framework, backend o build pipeline
2. **Accuratezza scientifica** — ogni numero deve avere fonte verificabile
3. **Trasparenza** — metadata completi su ogni dato
4. **Accessibilità** — la dashboard deve essere fruibile da tutti

### Come contribuire

1. Aprire una issue per discutere le modifiche
2. Creare un branch feature/ da main
3. Implementare le modifiche
4. Eseguire la validazione pre-commit
5. Aggiornare la documentazione se necessario
6. Fare PR su main

### Standard di codice

- HTML semantico, validato
- CSS organizzato per sezioni, con variabili custom
- JavaScript: dati centralizzati in oggetto DATA
- No dipendenze superflue
- No codice morto o commentato
- Testare sempre su mobile e desktop

### Validazione richiesta

Prima di ogni commit:
- HTML valido
- Nessun errore console
- Dati coerenti tra grafici e tabella
- Responsive funzionante
- Accessibilità base rispettata
