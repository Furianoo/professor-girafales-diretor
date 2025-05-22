import sqlite3
from datetime import datetime

# Criar banco em memória
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# ------------------- CRIAÇÃO DAS TABELAS -------------------
cursor.executescript('''
CREATE TABLE DEPARTMENT (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE PROFESSOR (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER);
CREATE TABLE TITLE (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE BUILDING (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE ROOM (id INTEGER PRIMARY KEY, name TEXT, building_id INTEGER);
CREATE TABLE SUBJECT (id INTEGER PRIMARY KEY, code TEXT, taught_by INTEGER);
CREATE TABLE CLASS (id INTEGER PRIMARY KEY, subject_id INTEGER, year INTEGER, semester INTEGER, code TEXT);
CREATE TABLE CLASS_SCHEDULE (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    room_id INTEGER,
    day_of_week TEXT,
    start_time TEXT,
    end_time TEXT
);
''')

# ------------------- INSERÇÃO DE DADOS -------------------
cursor.executescript('''
INSERT INTO DEPARTMENT VALUES (1, 'Matemática');
INSERT INTO PROFESSOR VALUES (1, 'Prof. Girafales', 1);
INSERT INTO PROFESSOR VALUES (2, 'Prof. Jirafinha', 1);
INSERT INTO BUILDING VALUES (1, 'Bloco A');
INSERT INTO ROOM VALUES (1, 'Sala 101', 1);
INSERT INTO ROOM VALUES (2, 'Sala 102', 1);
INSERT INTO SUBJECT VALUES (1, 'MAT101', 1);
INSERT INTO SUBJECT VALUES (2, 'MAT102', 2);
INSERT INTO CLASS VALUES (1, 1, 2025, 1, 'T1');
INSERT INTO CLASS VALUES (2, 2, 2025, 1, 'T2');
INSERT INTO CLASS_SCHEDULE VALUES (1, 1, 1, 'Segunda', '08:00', '10:00');
INSERT INTO CLASS_SCHEDULE VALUES (2, 1, 1, 'Quarta', '08:00', '10:00');
INSERT INTO CLASS_SCHEDULE VALUES (3, 2, 2, 'Terça', '10:00', '12:00');
''')

# ------------------- CONSULTA 1: HORAS COMPROMETIDAS -------------------
print("\n[1] Horas comprometidas por professor:")
cursor.execute('''
SELECT
    p.name AS professor,
    SUM(
        (CAST(strftime('%H', end_time) AS INTEGER)*60 + CAST(strftime('%M', end_time) AS INTEGER)) -
        (CAST(strftime('%H', start_time) AS INTEGER)*60 + CAST(strftime('%M', start_time) AS INTEGER))
    ) / 60.0 AS horas
FROM
    PROFESSOR p
JOIN SUBJECT s ON s.taught_by = p.id
JOIN CLASS c ON c.subject_id = s.id
JOIN CLASS_SCHEDULE cs ON cs.class_id = c.id
GROUP BY p.name;
''')
for row in cursor.fetchall():
    print(f"  Professor: {row[0]}, Horas: {row[1]:.1f}h")

# ------------------- CONSULTA 2: HORÁRIOS OCUPADOS -------------------
print("\n[2] Horários ocupados por sala:")
cursor.execute('''
SELECT r.name, cs.day_of_week, cs.start_time, cs.end_time
FROM ROOM r
LEFT JOIN CLASS_SCHEDULE cs ON cs.room_id = r.id
ORDER BY r.name, cs.day_of_week, cs.start_time;
''')
ocupados = {}
for sala, dia, ini, fim in cursor.fetchall():
    if sala not in ocupados:
        ocupados[sala] = {}
    if dia:
        ocupados[sala].setdefault(dia, []).append((ini, fim))
        print(f"  Sala: {sala}, Dia: {dia}, {ini} - {fim}")

# ------------------- LÓGICA DE HORÁRIOS LIVRES -------------------
print("\n[3] Horários livres por sala:")
HORARIO_ABERTURA = datetime.strptime('08:00', '%H:%M')
HORARIO_FECHAMENTO = datetime.strptime('18:00', '%H:%M')
dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']

for sala in ['Sala 101', 'Sala 102']:
    print(f"\n  Sala: {sala}")
    for dia in dias_semana:
        livres = []
        ocup = ocupados.get(sala, {}).get(dia, [])
        ocup = sorted([(datetime.strptime(i, '%H:%M'), datetime.strptime(f, '%H:%M')) for i, f in ocup])

        atual = HORARIO_ABERTURA
        for ini, fim in ocup:
            if atual < ini:
                livres.append((atual.strftime('%H:%M'), ini.strftime('%H:%M')))
            atual = max(atual, fim)

        if atual < HORARIO_FECHAMENTO:
            livres.append((atual.strftime('%H:%M'), HORARIO_FECHAMENTO.strftime('%H:%M')))

        if livres:
            print(f"    {dia}: {', '.join([f'{i}-{f}' for i, f in livres])}")
        else:
            print(f"    {dia}: Sem horários livres")

conn.close()
