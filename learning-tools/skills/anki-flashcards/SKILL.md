---
name: Anki Flashcards
description: Create effective Anki flashcards from text, documents, or images for spaced repetition learning
version: 0.2.0
---

# Anki Flashcards

Transform content into well-structured Anki flashcards optimized for long-term retention using spaced repetition principles. Based on Andy Matuschak's research on writing effective prompts.

## When to Use

Apply this skill when the user:
- Asks to "create flashcards" or "make Anki cards"
- Wants to study or memorize content
- Shares text, notes, or images and asks to turn them into study materials
- Requests help preparing for exams or learning new material
- Asks to "ankify" content

## Output Behavior

**Default Output:** Provide flashcards in Anki-compatible format directly in the response.

**Format:** Use tab-separated format (TSV) that can be directly imported into Anki:
```
Front<tab>Back
```

**For files:** When the user requests a file or there are many cards (10+), create a `.txt` file with tab-separated values that Anki can import directly.

**Include a summary** at the end showing the total card count and suggested deck name.

---

## The Five Attributes of Effective Prompts

Every prompt must be evaluated against these five properties:

### 1. Focused
Each prompt should focus on a single detail or atomic unit of knowledge. When scope is too broad, retrieval lacks a clear target.

**Too broad:** "What are the causes of World War I?"
**Focused:** "What 1914 assassination triggered World War I?" → "Assassination of Archduke Franz Ferdinand"

### 2. Precise
The prompt should be unambiguous about what it's asking. Vague questions produce vague learning.

**Imprecise:** "What about chicken stock?"
**Precise:** "What type of chicken parts are best for making stock?" → "Bones with some meat attached (backs, necks, wings)"

### 3. Consistent
The prompt should produce the same answer every time. If you find yourself giving different correct answers, the prompt needs revision.

**Inconsistent:** "Name an important JavaScript array method" → (could be map, filter, reduce, etc.)
**Consistent:** "What JavaScript array method creates a new array by applying a function to each element?" → "map()"

### 4. Tractable
You should be able to answer correctly almost every time. Prompts you consistently fail create frustration and should be broken down or given additional cues.

**Intractable:** "Recite the first 20 digits of pi"
**Tractable:** "What are the first 5 digits of pi after the decimal?" → "14159"

### 5. Effortful
The prompt must require actual retrieval from memory. You shouldn't be able to trivially infer the answer from the question.

**Too easy:** "Is the mitochondria the powerhouse of the cell?" → "Yes"
**Effortful:** "What organelle is called the powerhouse of the cell?" → "Mitochondria"

---

## Step-by-Step Process for Creating Cards

### Step 1: Classify the Knowledge Type

Identify what type of knowledge you're encoding:

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Discrete facts, definitions, terminology | "What year did WWII end?" |
| **Conceptual** | Relationships, causes, implications, mental models | "Why does inflation reduce purchasing power?" |
| **Procedural** | Steps, processes, how to do things | "What's the first step in CPR?" |

### Step 2: Identify What's Worth Encoding

Not everything deserves a card. Prioritize:
- Foundational knowledge that other concepts build upon
- Frequently needed information
- Easy-to-confuse details
- Knowledge that connects to things you actively think about

**Avoid orphan prompts:** Don't create cards for interesting but disconnected details. Prompts should connect to your existing knowledge and current interests.

### Step 3: Encode from Multiple Angles

A single fact should often become multiple cards that approach it differently:

**Original fact:** "The mitochondria produces ATP through oxidative phosphorylation"

**Multiple angles:**
- "What organelle produces most of a cell's ATP?" → "Mitochondria"
- "What process do mitochondria use to generate ATP?" → "Oxidative phosphorylation"
- "Where in the cell does oxidative phosphorylation occur?" → "Mitochondria"
- "What is the main product of oxidative phosphorylation?" → "ATP"

### Step 4: Apply Knowledge-Specific Strategies

#### For Factual Knowledge
- Use simple Q&A pairs
- Create bidirectional cards for terms/translations
- Add context to disambiguate

#### For Conceptual Knowledge
Use these "lenses" to generate prompts:
- **Attributes & tendencies:** "What property of water allows insects to walk on it?" → "Surface tension"
- **Similarities & differences:** "How does RNA differ from DNA in its sugar component?" → "RNA has ribose; DNA has deoxyribose"
- **Causes & effects:** "What causes inflation to reduce purchasing power?" → "More money chasing the same goods raises prices"
- **Significance & implications:** "Why is the double helix structure of DNA significant for replication?" → "Each strand serves as a template for copying"

#### For Procedural Knowledge
- Break procedures into individual steps
- Use cloze deletions for sequences
- Create "what comes next" prompts

**Example procedure (CPR):**
- "What's the first step when you find an unresponsive person?" → "Check for responsiveness and call for help"
- "In CPR, what do you do after calling 911?" → "Begin chest compressions"
- "How deep should chest compressions be for an adult?" → "At least 2 inches (5 cm)"

#### For Lists and Sets
- Create fill-in-the-missing-element prompts
- Keep order consistent to leverage spatial memory
- Break large lists into meaningful subcategories

**Example (planets):**
- "Name the planet: Mercury, Venus, Earth, _____, Jupiter" → "Mars"
- "Name the planet: _____, Venus, Earth, Mars, Jupiter" → "Mercury"
- "What are the four inner (terrestrial) planets?" → "Mercury, Venus, Earth, Mars"

### Step 5: Choose the Right Card Type

| Card Type | Best For | Syntax |
|-----------|----------|--------|
| **Basic Q&A** | Most factual knowledge | `Question → Answer` |
| **Reversed** | Vocabulary, bidirectional facts | Create two cards |
| **Cloze** | Definitions, sequences, fill-in-blank | `{{c1::answer}}` |

**Note on Cloze Deletions:** They're efficient to create but may produce less understanding than Q&A pairs. Use them for:
- Definitions where the structure helps
- Sequences and procedures
- When you need to create many cards quickly

Prefer Q&A pairs when deeper understanding matters.

### Step 6: Write the Cards

For each card, verify:
- [ ] Is it focused on ONE thing?
- [ ] Is the question precise and unambiguous?
- [ ] Will it produce consistent answers?
- [ ] Can I realistically answer it?
- [ ] Does it require actual recall (not inference)?

### Step 7: Create Connection Cards

Add prompts that link new knowledge to existing knowledge:
- "How does [new concept] relate to [known concept]?"
- "What's an example of [new concept] in [familiar domain]?"

### Step 8: Add Salience Prompts (Optional)

For ideas you want to keep top-of-mind for creative or practical application:
- "In what situations might [concept] be useful?"
- "How could [principle] apply to my work on [project]?"

These extend the "Baader-Meinhof phenomenon" deliberately.

---

## Handling Different Content Types

### Text/Notes
1. Read for understanding first
2. Identify key concepts, terms, and relationships
3. Apply the step-by-step process above
4. Focus on what's foundational or frequently needed

### Images/Diagrams
- Create identification prompts: "What structure is at position X?"
- Create function prompts: "What does the highlighted structure do?"
- Reference spatial relationships clearly
- Consider what would be tested in an exam

### Code/Technical Content
- Test syntax, method names, return values
- Focus on gotchas and commonly confused elements
- Include code snippets in monospace
- Create "what does this output?" prompts

### Language Learning
- Always create bidirectional cards
- Include example sentences for context
- Test grammar patterns with fill-in-blank
- Group by theme or difficulty level

---

## Revision and Improvement

During reviews, notice your reactions:
- **"I never remember this"** → Break into smaller cards or add cues
- **"I know the answer but don't understand it"** → Add conceptual cards
- **Internal sigh at a prompt** → Flag for revision

Most spaced repetition apps let you flag cards during review. After each session, revise flagged cards.

---

## Output Format Example

```
What is the capital of Japan?	Tokyo
What Japanese city was the imperial capital from 794 to 1868?	Kyoto
What process do mitochondria use to produce ATP?	Oxidative phosphorylation
Where in the cell does oxidative phosphorylation occur?	Mitochondria (inner membrane)
{{c1::Mitochondria}} are the organelles responsible for producing most cellular ATP	(cloze)
In Python, what method adds an element to the end of a list?	append()
[Reversed] append()	Python list method that adds an element to the end
```

## Additional Resources

- [references/patterns.md](references/patterns.md) - Examples across different subjects
- [Andy Matuschak's "How to write good prompts"](https://andymatuschak.org/prompts/) - The foundational guide this skill is based on
