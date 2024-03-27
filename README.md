Dette projekt dækker over uge 7+8 fra Specialisterne Academy 2024. 

I denne løsning anvendes OOP til at lave klasser for transaktioner, kategorier og varer. 

Her er bl.a. anvendt strategy design mønstret til søgningsmekanikken - denne endte dog ikke med at virke, og måtte istedet lade implementationen forblive ikke-funktionel af tidsmæssige årsager.
Af samme grund er funktionaliteten for at generere en rapport over forskellige varer heller ikke blevet implementeret så det er funktionelt, og er blevet nedprioriteret.

Singeton pattern er anvendt til oprettelse af database-forbindelse... her skal kun en enkelt database instans kunne være oprettet ad gangen. 

SOLID principperne er også til dels anvendt i denne løsning - herunder modularitet og single responsibility i opdelingen af klasserne og metoderne. 

I denne opgave er der i høj grad blevet lagt vægt fra min side på at kunne få en god forståelse for anvendelse af SQL workbench og stored procedures. 
Disse procedures kaldes alle igennem koden i klasserne for de forskellige tables. Dette er et design mæssigt valg for at opsplitte funktionaliteten yderligere.

med i dette github projekt ligger også en tilhørende SQL fil, som bør køres i sin lokale MYSQL workbench. Denne opretter både tables og stored procedures. 

Med andre ord, efter CRUD princippet var det operationerne i R som mangler at virke rigtigt,selvom forsøgt implementation er bevaret i denne besvarelse. 

Fremtidig lsning ville være at inkludere triggers til at håndtere rapport generering f.eks.
