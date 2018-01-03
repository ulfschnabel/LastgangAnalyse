#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 17:49:30 2018

@author: ulfschnabel
"""

 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
 
 #-----------------------------------------------------------------------------#
 # Mit diesem Script können die Feiertage in Deutschland berechnet und         #
 # ausgegeben werden. Wird dem Script ein Bundesland übergeben, werden alle    #
 # Feiertage dieses Bundeslandes ausgegeben. Wird kein Bundesland übergeben,   #
 # so werden nur die bundeseinheitlichen Feiertage ausgegeben.                 #
 #                                                                             #
 # Autor: Stephan John                                                         #
 # Version: 1.1                                                                #
 13 #                                                                             #
 12 # Datum: 25.05.2012                                                           #
 14 # Danke an Paul Wachendorf für die Hinweise                                   #
 15 #-----------------------------------------------------------------------------#
 16 
 17 
 18 import datetime
 19 
 20 state_codes = {
 21                 'Baden-Württemberg':'BW',
 22                 'Bayern':'BY',
 23                 'Berlin':'BE',
 24                 'Brandenburg':'BB',
 25                 'Bremen':'HB',
 26                 'Hamburg':'HH',
 27                 'Hessen':'HE',
 28                 'Mecklenburg-Vorpommern':'MV',
 29                 'Niedersachsen':'NI',
 30                 'Nordrhein-Westfalen':'NW',
 31                 'Rheinland-Pfalz':'RP',
 32                 'Saarland':'SL',
 33                 'Sachsen':'SN',
 34                 'Sachsen-Anhalt':'ST',
 35                 'Schleswig-Holstein':'SH',
 36                 'Thüringen':'TH',
 37                }
 38 
 39 def holidays(year, state=None):
 40 
 41     """
 42     prüft die eingegebenen Werte für die Berechnung der Feiertage
 43     year  => Jahreszahl ab 1970
 44     state => Bundesland als offizielle Abkürzung oder Vollname
 45     """
 46 
 47     try:
 48         year = int(year)
 49         if year < 1970:
 50             year = 1970
 51             print u'Jahreszahl wurde auf 1970 geändert'
 52     except ValueError:
 53         print u'Fehlerhafte Angabe der Jahreszahl'
 54         return
 55     if state:
 56         if state in state_codes.keys():
 57             state_code = state_codes[state]
 58         else:
 59             if state.upper() in state_codes.values():
 60                 state_code = state.upper()
 61             else:
 62                 state_code = None
 63     else:
 64         state_code = None
 65     if not state_code:
 66         print u'Es werden nur die deutschlandweit gültigen Feiertage ausgegeben'
 67     hl = Holidays(year, state_code)
 68     holidays = hl.get_holiday_list()
 69     for h in holidays:
 70         print h[1],  h[0]
 71 
 72 class Holidays:
 73 
 74     """
 75     Berechnet die Feiertage für ein Jahr. Wird ein Bundesland übergeben, werden
 76     alle Feiertage des Bundeslandes zurückgegeben. Das erfolgt über die
 77     Funktion get_holiday_list().
 78     Das Bundesland (state_code) muss mit der offiziellen zweistelligen
 79     Bezeichnung übergeben werden (z.B. Sachsen mit SN)
 80 
 81     Holidays(year(int), [state_code(str)])
 82     """
 83 
 84     def __init__(self, year, state_code):
 85         self.year = int(year)
 86         if self.year < 1970:
 87             self.year = 1970
 88         if state_code:
 89             self.state_code = state_code.upper()
 90             if self.state_code not in state_codes.values():
 91                 self.state_code = None
 92         easter_day = EasterDay(self.year)
 93         self.easter_date = easter_day.get_date()
 94         self.holiday_list = []
 95         self.general_public_holidays()
 96         if state_code:
 97             self.get_three_kings(state_code)
 98             self.get_assumption_day(state_code)
 99             self.get_reformation_day(state_code)
100             self.get_all_saints_day(state_code)
101             self.get_repentance_and_prayer_day(state_code)
102             self.get_corpus_christi(state_code)
103 
104     def get_holiday_list(self):
105 
106         """
107         Gibt die Liste mit den Feiertagen zurück
108         """
109 
110         self.holiday_list.sort()
111         return self.holiday_list
112 
113     def general_public_holidays(self):
114 
115         """
116         Alle bundeseinheitlichen Feiertage werden der Feiertagsliste
117         zugefügt.
118         """
119 
120         # feste Feiertage:
121         newyear = datetime.date(self.year, 1, 1)
122         self.holiday_list.append([newyear, u'Neujahr'])
123         may = datetime.date(self.year, 5, 1)
124         self.holiday_list.append([may, u'1. Mai'])
125         union = datetime.date(self.year, 10, 3)
126         self.holiday_list.append([union, u'Tag der deutschen Einheit'])
127         christmas1 = datetime.date(self.year, 12, 25)
128         self.holiday_list.append([christmas1, u'Erster Weihnachtsfeiertag'])
129         christmas2 = datetime.date(self.year, 12, 26)
130         self.holiday_list.append([christmas2, u'Zweiter Weihnachtsfeiertag'])
131         #bewegliche Feiertage:
132         self.holiday_list.append([self.get_holiday(2, _type='minus'), u'Karfreitag'])
133         self.holiday_list.append([self.easter_date, u'Ostersonntag'])
134         self.holiday_list.append([self.get_holiday(1), u'Ostermontag'])
135         self.holiday_list.append([self.get_holiday(39), u'Christi Himmelfahrt'])
136         self.holiday_list.append([self.get_holiday(49), u'Pfingstsonntag'])
137         self.holiday_list.append([self.get_holiday(50), u'Pfingstmontag'])
138 
139 
140     def get_holiday(self, days, _type='plus'):
141 
142         """
143         Berechnet anhand des Ostersonntages und der übergebenen Anzahl Tage
144         das Datum des gewünschten Feiertages. Mit _type wird bestimmt, ob die Anzahl
145         Tage addiert oder subtrahiert wird.
146         """
147 
148         delta = datetime.timedelta(days=days)
149         if _type == 'minus':
150             return self.easter_date - delta
151         else:
152             return self.easter_date + delta
153 
154     def get_three_kings(self, state_code):
155         """ Heilige Drei Könige """
156         valid = ['BY', 'BW', 'ST']
157         if state_code in valid:
158             three_kings = datetime.date(self.year, 1, 6)
159             self.holiday_list.append([three_kings, u'Heilige Drei Könige'])
160 
161     def get_assumption_day(self, state_code):
162         """ Mariä Himmelfahrt """
163         valid = ['BY', 'SL']
164         if state_code in valid:
165             assumption_day = datetime.date(self.year, 8, 15)
166             self.holiday_list.append([assumption_day, u'Mariä Himmelfahrt'])
167 
168     def get_reformation_day(self, state_code):
169         """ Reformationstag """
170         valid = ['BB', 'MV', 'SN', 'ST', 'TH']
171         if state_code in valid:
172             reformation_day = datetime.date(self.year, 10, 31)
173             self.holiday_list.append([reformation_day, u'Reformationstag'])
174 
175     def get_all_saints_day(self, state_code):
176         """ Allerheiligen """
177         valid = ['BW', 'BY', 'NW', 'RP', 'SL']
178         if state_code in valid:
179             all_saints_day = datetime.date(self.year, 11, 1)
180             self.holiday_list.append([all_saints_day, u'Allerheiligen'])
181 
182     def get_repentance_and_prayer_day(self, state_code):
183         """
184         Buß und Bettag
185         (Mittwoch zwischen dem 16. und 22. November)
186         """
187         valid = ['SN']
188         if state_code in valid:
189             first_possible_day = datetime.date(self.year, 11, 16)
190             rap_day = first_possible_day
191             weekday = rap_day.weekday()
192             step = datetime.timedelta(days=1)
193             while weekday != 2:
194                 rap_day = rap_day + step
195                 weekday = rap_day.weekday()
196             self.holiday_list.append([rap_day, u'Buß und Bettag'])
197 
198     def get_corpus_christi(self, state_code):
199         """
200         Fronleichnam
201         60 Tage nach Ostersonntag
202         """
203         valid = ['BW','BY','HE','NW','RP','SL']
204         if state_code in valid:
205             corpus_christi = self.get_holiday(60)
206             self.holiday_list.append([corpus_christi, u'Fronleichnam'])
207 
208 
209 
210 class EasterDay:
211 
212     """
213     Berechnung des Ostersonntages nach der Formel von Heiner Lichtenberg für
214     den gregorianischen Kalender. Diese Formel stellt eine Zusammenfassung der
215     Gaußschen Osterformel dar
216     Infos unter http://de.wikipedia.org/wiki/Gaußsche_Osterformel
217     """
218 
219     def __init__(self, year):
220         self.year = year
221 
222     def get_k(self):
223 
224         """
225         Säkularzahl:
226         K(X) = X div 100
227         """
228 
229         k = self.year / 100
230         return k
231 
232     def get_m(self):
233 
234         """
235         säkulare Mondschaltung:
236         M(K) = 15 + (3K + 3) div 4 − (8K + 13) div 25
237         """
238 
239         k = self.get_k()
240         m = 15 + (3 * k + 3) / 4 - (8 * k + 13) / 25
241         return m
242 
243     def get_s(self):
244 
245         """
246         säkulare Sonnenschaltung:
247         S(K) = 2 − (3K + 3) div 4
248         """
249 
250         k = self.get_k()
251         s = 2 - (3 * k + 3) / 4
252         return s
253 
254     def get_a(self):
255 
256         """
257         Mondparameter:
258         A(X) = X mod 19
259         """
260 
261         a = self.year % 19
262         return a
263 
264     def get_d(self):
265 
266         """
267         Keim für den ersten Vollmond im Frühling:
268         D(A,M) = (19A + M) mod 30
269         """
270 
271         a = self.get_a()
272         m = self.get_m()
273         d = (19 * a + m) % 30
274         return d
275 
276     def get_r(self):
277 
278         """
279         kalendarische Korrekturgröße:
280         R(D,A) = D div 29 + (D div 28 − D div 29) (A div 11)
281         """
282 
283         a = self.get_a()
284         d = self.get_d()
285         r = d / 29 + (d / 28 - d / 29) * (a / 11)
286         return r
287 
288     def get_og(self):
289 
290         """
291         Ostergrenze:
292         OG(D,R) = 21 + D − R
293         """
294 
295         d = self.get_d()
296         r = self.get_r()
297         og = 21 + d - r
298         return og
299 
300     def get_sz(self):
301 
302         """
303         erster Sonntag im März:
304         SZ(X,S) = 7 − (X + X div 4 + S) mod 7
305         """
306 
307         s = self.get_s()
308         sz = 7 - (self.year + self.year / 4 + s) % 7
309         return sz
310 
311     def get_oe(self):
312 
313         """
314         Entfernung des Ostersonntags von der Ostergrenze
315         (Osterentfernung in Tagen):
316         OE(OG,SZ) = 7 − (OG − SZ) mod 7
317         """
318 
319         og = self.get_og()
320         sz = self.get_sz()
321         oe = 7 - (og - sz) % 7
322         return oe
323 
324     def get_os(self):
325 
326         """
327         das Datum des Ostersonntags als Märzdatum
328         (32. März = 1. April usw.):
329         OS = OG + OE
330         """
331 
332         og = self.get_og()
333         oe = self.get_oe()
334         os = og + oe
335         return os
336 
337     def get_date(self):
338 
339         """
340         Ausgabe des Ostersonntags als datetime-Objekt
341         """
342 
343         os = self.get_os()
344         if os > 31:
345             month = 4
346             day = os - 31
347         else:
348             month = 3
349             day = os
350         easter_day = datetime.date(self.year, month, day)
351         return easter_day
352 
353 if __name__ == '__main__':
354     y = raw_input('Bitte geben Sie die Jahreszahl ein: ')
355     print u'Für die Eingabe eines Bundeslandes folgende Abkürzungen verwenden:'
356     print u'< leer > um kein Bundesland auszuwählen'
357     states = state_codes.keys()
358     states.sort()
359     for l in states:
360         print '%s für %s'%(state_codes[l], l)
361     s = raw_input('Bitte geben Sie das gewünschte Bundesland ein: ')
362     holidays(y, s)