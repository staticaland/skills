# Anki Flashcard Patterns

Examples of effective flashcard creation across different subjects and content types.

## Science Examples

### Original Text
> "The mitochondria are membrane-bound organelles found in the cytoplasm of eukaryotic cells. They generate most of the cell's supply of ATP through oxidative phosphorylation."

### Generated Cards
```
What organelle generates most of the cell's ATP?	Mitochondria
Where in the cell are mitochondria located?	In the cytoplasm
What process do mitochondria use to generate ATP?	Oxidative phosphorylation
Mitochondria are found in what type of cells?	Eukaryotic cells
{{c1::Mitochondria}} generate most of the cell's ATP through {{c2::oxidative phosphorylation}}	(cloze)
```

---

## Programming Examples

### Original Text
> "In JavaScript, the `map()` method creates a new array populated with the results of calling a provided function on every element in the calling array. It does not mutate the original array."

### Generated Cards
```
In JavaScript, what method applies a function to every array element and returns a new array?	map()
Does JavaScript's map() method mutate the original array?	No, it returns a new array
What is the return value of array.map()?	A new array with transformed elements
[JavaScript] Complete: const doubled = numbers._____(n => n * 2)	map
```

---

## History Examples

### Original Text
> "The French Revolution began in 1789 with the storming of the Bastille. It led to the end of absolute monarchy and the rise of Napoleon Bonaparte."

### Generated Cards
```
What event marked the beginning of the French Revolution?	The storming of the Bastille
In what year did the French Revolution begin?	1789
What system of government ended as a result of the French Revolution?	Absolute monarchy
Who rose to power following the French Revolution?	Napoleon Bonaparte
The storming of the {{c1::Bastille}} in {{c2::1789}} marked the start of the French Revolution	(cloze)
```

---

## Language Learning Examples

### Spanish Vocabulary
```
house (English to Spanish)	casa
casa (Spanish to English)	house
The house is big. (Translate to Spanish)	La casa es grande.
```

### Grammar Rules
```
When do you use "ser" vs "estar" for location?	Use "estar" for location (temporary state)
[Spanish] Conjugate "hablar" in first person present	hablo
```

---

## Medical/Anatomy Examples

### From an Anatomy Diagram
```
What structure connects the stomach to the small intestine?	Pyloric sphincter
Name the three sections of the small intestine in order	Duodenum, jejunum, ileum
The {{c1::duodenum}} is the first section of the small intestine	(cloze)
```

---

## Mathematics Examples

### Original Content
> "The quadratic formula solves ax² + bx + c = 0: x = (-b ± √(b²-4ac)) / 2a"

### Generated Cards
```
What formula solves quadratic equations of the form ax² + bx + c = 0?	x = (-b ± √(b²-4ac)) / 2a
In the quadratic formula, what is the discriminant?	b² - 4ac
If the discriminant is negative, what type of solutions does the quadratic have?	Complex/imaginary solutions
If the discriminant equals zero, how many real solutions does the quadratic have?	One (repeated root)
```

---

## Anti-Patterns to Avoid

### Too Vague
**Bad:** "Explain DNA" → "DNA is genetic material..."
**Better:** "What molecule carries genetic information in cells?" → "DNA (deoxyribonucleic acid)"

### Multiple Facts per Card
**Bad:** "What are the stages of mitosis and what happens in each?" → [long paragraph]
**Better:** Create separate cards for each stage

### Answer in the Question
**Bad:** "Is the mitochondria the powerhouse of the cell?" → "Yes"
**Better:** "What organelle is known as the powerhouse of the cell?" → "Mitochondria"

### Too Much Text on Back
**Bad:** "What is HTTP?" → [3 paragraphs]
**Better:** "What does HTTP stand for?" → "HyperText Transfer Protocol"

---

## Image-Based Card Examples

When processing images like diagrams or charts, create cards like:

### Anatomy Diagram
```
[Referring to heart diagram] What chamber receives blood from the body?	Right atrium
[Referring to heart diagram] What vessel carries blood from the heart to the lungs?	Pulmonary artery
```

### Flowchart/Process Diagram
```
[Referring to water cycle diagram] What process moves water from oceans to atmosphere?	Evaporation
[Referring to water cycle diagram] What comes after condensation in the water cycle?	Precipitation
```

### Map
```
[Referring to map] What country borders France to the northeast?	Belgium
[Referring to map] What mountain range separates France from Spain?	Pyrenees
```

---

## Suggested Tags by Subject

Use tags to organize cards in Anki:

- `#biology #cell-structure`
- `#javascript #arrays #methods`
- `#history #french-revolution #18th-century`
- `#spanish #vocabulary #a1`
- `#anatomy #digestive-system`
- `#math #algebra #quadratic`
