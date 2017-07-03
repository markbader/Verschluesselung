from tkinter import Tk, Text, Menu, filedialog, Scrollbar, Frame, Toplevel, Label, Button, Entry, messagebox
root=Tk()       #das Fenster root wird erschaffen
root.title('Verschlüsselung')   #Dem Fenster wird der Titel Verschlüsselung gegeben
root.resizable(width='no', height='no')     #Die groeße des Fensters soll sich nicht verändern lassen

def create_menu():      #erstellt ein Menue am oberen Fensterrand
    try:
        menu = Menu(root)       #erstellt eine Instanz der Klasse Menu
        file_menu=Menu(menu,tearoff=0)      #erstellt ein Untermenue
        file_menu.add_command(label='Neu', command=new_file)
        file_menu.add_command(label='Öffnen...',command=open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Speichern unter...', command=save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='Schließen', command=root.destroy)
        menu.add_cascade(label='Datei', menu=file_menu)
        edit_menu=Menu(menu,tearoff=0)
        edit_menu.add_command(label='Kopieren', command=copy_selected_text)
        edit_menu.add_command(label='Ausschneiden', command=cut_selected_text)
        edit_menu.add_command(label='Einfügen', command=paste)
        edit_menu.add_separator()
        edit_menu.add_command(label='Alles Markieren', command=select_all)
        menu.add_cascade(label='Bearbeiten', menu=edit_menu)
        text_menu=Menu(menu,tearoff=0)
        text_menu.add_command(label='Codieren', command=codieren)
        text_menu.add_separator()
        text_menu.add_command(label='Decodieren', command=decodieren)
        menu.add_cascade(label='Text', menu=text_menu)
        root.config(menu=menu)      
    except:
        print('Fehler: Ein unerwarteter Fehler ist aufgetreten')

def new_file():         #loescht den gesamten Inhalt des Textfeldes
    text.delete('1.0','end')

def open_file():        #der Benutzer kann durch ein Dialogfenster die Datei auswählen die er öffnen möchte
    datei_suchen=filedialog.askopenfilename(filetypes=[('Text-Dateien', '*.txt'),('Alle Datein','*.*')])      #Dialogfenster für Dateiauswahl
    try:
        datei_lesen=open(datei_suchen, 'r')     #ausgewählte Datei wird aufgerufen
        datei_gelesen=datei_lesen.read()        #der Inhalt der Datei wird gelesen
        text.config(state='normal')
        text.delete('1.0', 'end')               #Text aus dem Textfeld wird gelöscht
        text.insert('1.0', datei_gelesen)       #Text aus der Datei wird in Textfeld eingefügt
        datei_lesen.close()
    except:
        print('Fehler: Ein Fehler beim Öffnen ist ist aufgetreten')

def select_all():       #der Text in dem Textfeld wird Markiert
    text.tag_add('sel',"1.0", 'end')        #Der gesamte Text im Textfeld wird markiert
    text.mark_set('insert',"1.0")           #Der blinkende Strich wird zum Anfang der Auswahl gesetzt

def save_as_file():     #der Benutzer kann durch ein Dialogfenster die einen Ort und einen Namen
                        #auswählen und dann den Inhalt des Textfeldes unter dem Namen an dem Ort speichern
    ordner_suchen=filedialog.asksaveasfilename(title='Speichern', initialfile='Unbenannt.txt', \
                                               filetypes=[('Text-Dateien', '*.txt'),('Alle Datein','*.*')])
    try:
        zeichenanzahl=len(ordner_suchen)
        endung_pruefen=str(ordner_suchen[zeichenanzahl-4]+ordner_suchen[zeichenanzahl-3]\
                           +ordner_suchen[zeichenanzahl-2]+ordner_suchen[zeichenanzahl-1])
        if endung_pruefen=='.txt':      #prueft ob der Benutzer bereits ein Endung eingegeben hat
            datei_schreiben=open(ordner_suchen, 'w') #schreibt die Datei ohne eine Endung anzuhängen
            datei_geschrieben=datei_schreiben.write(str(text.get('1.0', 'end')))
            datei_schreiben.close()
        else:
            datei_schreiben=open(ordner_suchen+'.txt', 'w') #hängt eine Endung (.txt) an und schreibt die Datei
            datei_geschrieben=datei_schreiben.write(str(text.get('1.0', 'end')))
            datei_schreiben.close()
    except:
        print('Fehler: Ein Fehler beim Speichern ist aufgetreten') 

def copy_selected_text():   #der vom Benutzer ausgewählte Text wird in die Zwischenablage kopiert
    try:
        root.clipboard_clear()      #löscht den Inhalt der Zwischenablage
        t=text.get('sel.first','sel.last')  #nimmt sich den Ausgewählten Text
        root.clipboard_append(t)            #schreibt den Text in die Zwischenablage
    except:
        print('Fehler: Kein Text ausgewählt')

def codieren():         #der Text der in dem Textfeld steht wird mit Hilfe eines Codes bzw. eines Passwortes verschlüsselt
    try:
        t=text.get('1.0','end')     #der Textfeld inhalt wird Variable t zugeordnet
        if t[0:3]=='}~§':
            print('Fehler: Ungültige Zeichen im Textfeld')
        else:           #Um beim decodieren zu testen ob der Text nicht schon entschlüsselt ist werden kontroll zeichen hinzugefügt
            t='}~§'+t
            a=open('code.txt', 'r')     #Die Datei mit dem Passwort wird geoeffnet
            password=a.read()           #Der Inhalt der Datei wird zu einem String
            password=password.strip()
            a.close()
            tl=[]
            for i in t:
                tl.append(i)            #Der Text aus dem Textfeld wird in eine Liste umgewandelt
            for i in range(len(tl)):    #verschlüsselt den Text mit einer Caesar Verschlüsselung, jedoch wird das alphabet
                n=ord(password[i%len(password)])
                tl[i]=chr((ord(tl[i])+n)%110000)
            t=''
            for i in tl:        #Wandelt die Liste wieder in einen String um
                t+=i
        text.delete('1.0','end')        #Loescht den Textfeld inhalt
        text.insert('1.0',t)        #Der Codierte Text wird in das Textfeld eingefügt
    except:
        messagebox.showinfo('Fehler','Der Text konnte nicht verschlüsselt werden. Überprüfen sie ob sich eine Schlüsseldatei "code.txt" im gleichen Ordner befindet.')
        print('Fehler: Beim Verschlüsseln ist ein Fehler aufgetreten.')

def decodieren():       #der Text in dem Textfeld wird wieder entschlüsselt
    try:
        t=text.get('1.0','end')     #der Text aus dem Textfeld wird entnommen
        a=open('code.txt', 'r')     #die Datei mit dem Passwort wird geöffnet
        password=a.read()           #wird in einen String umgewandelt
        password=password.strip()   #nicht darstellbare Zeichen werden entfernt
        a.close()
        tl=[]
        for i in t:         #Text wird in Liste umgewandelt
            tl.append(i)
        for i in range(len(tl)):        #Der Text wird wieder decodiert
            n=ord(password[i%len(password)])
            tl[i]=chr((ord(tl[i])-n)%110000)
        t=''        #der decodierte Text wird in einen String umgewandelt
        for i in tl:
            t+=i
        if t[0:3]=='}~§':       #Wenn die sicherungszeichen dastehen wird der Text im Textfeld angezeigt
            t=t[3:len(t)]
            text.delete('1.0','end')
            text.insert('1.0',t[0:len(t)-2])
        else:       #Ansonsten wird ein Fehler geprintet
            print('Fehler: Der Text kann nicht entschlüsselt werden')
    except:
        messagebox.showinfo('Fehler','Beim entschlüsseln ist ein Fehler aufgetreten. Möglicherweise haben sie eine Falsche Datei zum Entschlüsseln verwendet.')
        print('Fehler: Beim Verschlüsseln ist ein Fehler aufgetreten.')
def cut_selected_text():        #Der vom Benutzer markierte Text wird ausgeschnitten
    try:
        copy_selected_text()    #Text wird in zwischenablage kopiert
        text.delete('sel.first','sel.last')     #der markierte Text wird entfernt
    except:
        print('Fehler: Kein Text ausgewählt')

def paste():            #Der inhalt der Zwischenablage wird eingefuegt
    try:
        t = root.selection_get(selection='CLIPBOARD')   #Zwischenablage wird ausgelesen
        text.insert('insert', t)    #der Inhalt der zwischenablage wird in das Textfeld geschrieben
    except:
        print('Fehler: Ein Fehler beim Einfügen ist aufgetreten')

create_menu()       #Menue wird erstellt
f1=Frame(root)      #Ramen wird erstellt
text=Text(f1)       #Textfeld wird erzeugt
text.focus_set()    #der blinkende Balken wird ins Textfeld gesetzt
scr=Scrollbar(f1, command=text.yview, relief='groove')  #eine Scrollleiste wird erstellt
text.config(yscrollcommand=scr.set)     #die Scrollleiste soll für Textfeld zustaendig sein
scr.pack(side='right',fill='y')     #Die Scrollleiste wird in dem Ramen rechts platziert
text.pack(fill='both', side='right')    #Das Textfeld wird neben der Scrollleiste platziert
f1.pack(fill='both')        #Der Rahmen mit seinem Inhalt wird im Fenster dargestellt
root.mainloop()     #Das Programm wird offen gehalten und wartet auf Benutzereingaben
