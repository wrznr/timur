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

- Operanden:
    + **freie Morpheme**: isoliert auftretende Wörter/Wortbestandteile (*Stamm*)
    + **gebundene Morpheme**: nur in Kombination mit freien Morphemen auftretende Wörter/Wortbestandteile (*Affix*)
    + **Zwischenstatus**: nicht isoliert auftretende Wortstämme (*Formativ*)
- Prozesse
    + **Flexion**: Kombination eines Wortes mit einem oder mehreren Affixen zur Erfüllung morphosyntaktischer Umgebungsanforderungen
    + **Derivation**: Kombination eines freien Morphems mit einem Affix zur Änderung von Wortart und/oder Bedeutung
    + **Konversion**: Änderung der Wortart eines Stammes **ohne** Affixinvolvierung
    + **Komposition**: Kombination zweier freier Morpheme

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
   ↦ Ärztekammer<NN>
   ↦ Ärzte#kammer~n
   ↦ Arzt<NN>Kammer<NN>
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

# Morphologische Analyse

- Schwachpunkte des Ansatzes:
    + Tendenz zur **Übergenerierung**
        * wenige echt produktive Derivationsprozesse!
    + hoher Aufwand bei der **Lexikonpflege**
        * wenige echt produktive Derivationsprozesse!
    + nicht robust
    + **flache Analyse** nicht für alle Anwendungsfälle adäquat
    + Modellierung 
- Vorteile des Ansatzes:
    + schnell (i.e. linear zur Eingabelänge)
    + rel. kompakt (i.e. quadratisch zur Lexikongröße)

---

# timur

- **Schlüsselfakten**:
    + Morphologisches Analysesystem auf Basis endlicher Automaten
        * zugeschnitten auf Wortzerlegung
    + Weiterentwicklung/Konsolidierung einer Wortgrammatik von Helmut Schmid
    + Implementierung in Python mit Hilfe von `pynini`, einer Python-API zu `OpenFst`
    + Open-Source-Entwicklung auf GitHub
- **Motivation**: Es fehlt an Alternativen!
    + wissenschaftlich längst gelöstes Problem
    + begrenzte Verfügbarkeit existierender Werkzeuge (hoher Aufwand bei Lexikonerstellung und -pflege?)
    + veraltete Architekturen für Implementierung und Nutzung

---

# timur im Vergleich

| Software | **TAGH** | **SMOR** | **Morphisto** | **Zmorge** | **timur** |
|:------|:----------:|:--------:|:-------:|:-------------:|:-------------------:|
| OpenSource Framework | (✓) | ✓ | ✓ | ✓ | ✓ |
| OpenSource Lexikon | ✗ | ✗ | ✓ | (✓) | ✓ |
| OpenSource Grammatik | ✗ | (✓) | ✓ | ✓ | ✓ | 
| komplexe Lexikoneinträge| ✓ | ✓ | ✓ | ✓ | ✗ |
| letzte Version | 2017 | 2013 | 2011 | 2015 | 8. Mai 2019 |

---

# timur -- Lexikon

- entstanden auf Basis einer großen Wortliste
    + Wortart
    + **DMOR**-Flexionsklasse (Schiller 1996)
- überarbeitet/annotiert in Kooperation mit Forschungsgruppe REaD (Sascha Schroeder)
    + morphologische Komplexität
    + Bildungsmuster
- Zahlen:
    + 11 989 **Adjektive** davon 774 Simplizia
    + 5 818 **Verben** davon 1 353 Simplizia
    + 24 107 **Nomen** davon 6 105 Simplizia

---

# timur -- Lexikon

| Wort | *Wortart* | *Flexionsklasse* | *komplex?* | *Bildung* |
|:------|:----------:|:--------:|:-------:|:-------------:|
| Acht | `NN` | `NFem/Sg` | ✗ | - |
| achten | `V` | `VVReg` | ✓ | `NN` |
| Achtung | `NN` | `NFem-Deriv` | ✓ | `V + ung` |
| achtbar | `ADJ` | `Adj+` | ✓ | `V + bar` |
| Achtbarkeit | `NN` | `NFem-Deriv` | ✓ | `ADJ + keit` |
| ächten | `V` | `VVReg` | ✓ | `NN$` |
| achtenswert | `ADJ` | `Adj+e` | ✓ | `NN + wert` |

- Ziel: Erstellung einer Baumstruktur pro Simplex

---

# timur -- Lexikon

<center><img src="img/tree.svg" style="position:absolute;top:200px;left:0;width:1200px;height:1200px" /></center>

---

# timur -- Lexikon

- Ziel:
    + Erstellung einer Baumstruktur pro Simplex
    + abhängig von der gewählten Kodierungsstrategie
        * Konvertierung der Lexikoneinträge in **automatenverarbeitbares** Format
        * Gestalt eines komplexen Eintrags abhängig von der Gestalt seines „Vorgängers”
- Herausforderungen:
    + **Lücken** in der Ableitungshierarchie
       * insbesondere im Bereich latinater Wortbildung (*inkommensurabel*)
       * und bei nicht-produktiven Ableitungen produktiv ableitbarer Wörter (*argusäugig*)
    + Ableitungen aus **Formativen** (*Amphitheater*)
    + **Pseudo-** bzw. synchron intransparente Derivationen (*verschwenden*)

---

# timur -- Grammatik

- basierend auf einer Beispielgrammatik von Helmut Schmid
    + auch für `Morphisto` und `Zmorge` genutzt
    + SFST-Format
- Transduktoren für
    + Lexikon
        * Basiseinträge
        * **Affixe**
    + Flexion (Suffixe + Filter)
    + Derivation (Filter)
    + Komposition (Filter)
    + Konversion (Konstruktionsregeln)

---

# timur -- Grammatik

```
<Base_Stems>Arzt<NN><base><nativ><NMasc_es_$e>
<ge><Base_Stems>lern<V><base><nativ><VVReg>
<Kompos_Stems>Ende:<epsilon><NN><kompos><nativ>
<Deriv_Stems>er<Pref>tra:äg<V><deriv><nativ>
<Suff_Stems><prefderiv,simplex,suffderiv><fremd,nativ><deriv><NN>chen<NN><SUFF><base><nativ><NNeut-Dimin>
<Suff_Stems><prefderiv,simplex,suffderiv><fremd,nativ><deriv><NN>chen<NN><SUFF><kompos><nativ>
<Suff_Stems><prefderiv,simplex,suffderiv><fremd,nativ><kompos><NN>los<ADJ><SUFF><base><nativ><Adj+e>
<no-ge><Pref_Stems>zer<PREF><V><nativ>
<Pref_Stems>durch<PREF><V><nativ>
```

- Σ
    + `<X>`: komplexe Symbole
    + `x`: Zeichen
