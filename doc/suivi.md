à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Application pour jouer en ligne au poker
* **Tuteur / Tutrice** : Lucas Bouju 
* [Dépôt GitHub](https://github.com/tomdtd/ENSAI-2A-projet-info-Albane-Tom-Neville-Floraline.git)

# :dart: Échéances

---
Dossier d'Analyse :  :clock1: <iframe src="https://free.timeanddate.com/countdown/i83zdl7u/n1264/cf11/cm0/cu2/ct4/cs0/ca0/co0/cr0/ss0/cac009/cpcf00/pcfff/tcfff/fs100/szw256/szh108/iso2025-10-07T12:00:00" allowtransparency="true" frameborder="0" width="130" height="16"></iframe>

---

```mermaid
gantt
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt
    %%excludes  YYYY-MM-DD and/or sunday and/or weekends 
     
    section Suivi
    TP1 et Suivi 1               :milestone, 2025-08-29,
    TP2 et Suivi 2               :milestone, 2025-09-05,
    TP3 et Suivi 3               :milestone, 2025-09-12,
    TP4                          :milestone, 2025-09-19,
    Suivi 4                      :milestone, 2025-10-03,
    3j immersion et suivi 5 et 6 :done,    2025-11-04, 3d
    Suivi 7                      :milestone, 2025-11-14,
    
    section Rendu
    Dossier Analyse              :milestone, 2025-09-27,
    Rapport + Code               :milestone, 2025-11-22,
    Soutenance                   :milestone, 2025-12-10,
    
    section Vac
    Toussaint                    :crit,    2025-10-25, 2025-11-02
    
    section Analyse
    Lancement du projet          :done,      2025-08-29, 7d
    étude préalable              :done,    2025-08-29, 15d
    rédaction                    :done,    2025-08-29, 30d
    relecture                    :done,    2025-09-20, 6d
    
    section Code
    lister les classes à coder   :done,    2025-09-15, 7d
    coder une v0 des classes     :done,    2025-09-19, 30d
```

# :calendar: Livrables

| ------- | ------------------------------------------------------------ |
| 27 sep. | [Dossier d'Analyse](https://www.overleaf.com/)               |
| 22 nov. | Rapport final + code |
| 10 déc. | Soutenance                                                    |

# :construction: Todo List

## Dossier Analyse

* [x] Diagramme de Gantt
* [x] Diagramme de cas d'utilisation
* [x] Diagramme C4
* [x] Diagramme de classe

## Code

* [x] Business Layer
* [x] Service Layer
* [x] DAO Layer
* [x] Web service
* [x] Controller Layer

---

* [x] appel WS
* [x] création WS

---

<style>h1 {
    color: darkblue;
    font-family: "Calibri";
    font-weight: bold;
    background-color: seagreen;
    padding-left: 10px;
}

h2 {
    color: darkblue;
    background-color: darkseagreen;
    margin-right: 10%;
    padding-left: 10px;
}

h3 {
    color: darkblue;
    background-color: lightseagreen;
    margin-right: 20%;
    padding-left: 10px;
}

h4 {
    color: darkblue;
    background-color: aquamarine;
    margin-right: 30%;
    padding-left: 10px;
}

</style>
