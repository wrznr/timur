layout: true

<div class="my-header"></div>

<div class="my-footer">
  <table>
    <tr>
      <td>timur: Finite-state morphology for German</td>
      <td style="text-align:right"><a href="https://wrznr.github.io/timur/">wrznr.github.io/timur</a></td>
    </tr>
  </table>
</div>

---

class: title-slide

# timur

## Morphologische Zerlegung mittels endlicher Automaten

Kay-Michael Würzner
[wuerzner@bbaw.de](mailto:wuerzner@bbaw.de)

---

# Überblick

- Morphologische Analyse
- timur
    + grundlegende Ideen
    + Implementierung
    + aktueller Stand
- Anwendungen
- Diskussion und Ausblick

---

# Morphologische Analyse

- Aufgaben
    + Bestimmung der **möglichen** Wortarten eines Wortes
      ```
      grünen ↦ {Verb, Adjektiv}
      Müller ↦ {Substantiv, Eigenname}
      ```
    + Abbildung auf eine kanonische **Grundform** (*Lemma*)
      ```
      grünen  ↦ grün
      Müllers ↦ Müller
      ```
    + Identifikation der beteiligten Wortbildungsprozesse
      ```
      Grünspan ↦ grün<A>Span<N>
      verirren ↦ ver<p>irren<V>
      ```
---

# Morphologische Analyse

- Analyseebenen
    + **Oberfläche**: sichtbare Gestalt der einzelnen Morpheme (i.e. Morphe)
        * phonotaktische Prozesse (Fugenelemente, Ab- und Umlaut)
        * Flexion
    + **Tiefe**: (abstrakte) Repräsentation aller Morpheme
- Anwendungsbezug
    + z.B. morphologische Zerlegung
        * Einschätzung der Bildungsproduktivität einzelner Morpheme: Tiefe
        * Unterstützung der Wortrennung: Oberfläche
    + z.B. Grundformbildung
        * Oberfläche **plus** Tiefe
```
Ärztekammern:
    Ärztekammer
    Ärzte#kammer~n
    Arzt<NN>Kammer<NN>
```

---

# Morphologische Analyse

- Verfahren des maschinellen Lernens nicht geeignet
- Herausfordend für Sprachen mit komplexer Wortbildung
- `Finite State Morphology` (klassischer regelbasierter Ansatz):
    + Man nehme
        * eine **große** Liste einfacher Wörter
        * deren **morphosyntaktische** Eigenschaften
        * Vor- und Nachsilben,
    + packe dies in einen **endlichen Automaten** und
    + bilde dessen **Kleenesche Hülle**
- Bestandteil der meisten Sprachverarbeitungssysteme

---

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

.center[.img-orig[![Lexikon](img/morph_ex.svg)]]

---

count: false

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

.center[.img-orig[![Lexikon](img/morph_ex2.svg)]]

---

count: false

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

<center><img src="img/morph_ex3.svg" width="650" /></center>

---

count: false

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

<center><img src="img/morph_ex4.svg" width="880" /></center>

---

count: false

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

<center><img src="img/morph_ex6.svg" width="880" /></center>

---

count: false

# Morphologische Analyse

- Illustration
    + Lexikon `{schön<A>,Geist<N>}`
    + Vorsilben `{un<p>,ur<p>}`
    + Nachsilben `{heit<N>,lich<A>}`

<center><img src="img/morph_ex5.svg" width="880" /></center>

---
