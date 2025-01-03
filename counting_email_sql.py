import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
csr = conn.cursor()

csr.execute('DROP TABLE IF EXISTS Counts')

csr.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = input('Enter file:')
if (len(fname)<1): fname = 'mbox.txt'

fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    csr.execute('SELECT count FROM Counts WHERE email=?', (email,))
    row = csr.fetchone()
    if row is None:
        csr.execute('''INSERT INTO Counts (email, count) VALUES (?, 1)''', (email,))
    else:
        csr.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))
    conn.commit()

#https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in csr.execute(sqlstr):
    print(str(row[0]), row[1])

csr.close()