---
name: Anki Flashcards
description: Create effective Anki flashcards from text, documents, or images for spaced repetition learning
version: 0.1.0
---

# Anki Flashcards

Transform content into well-structured Anki flashcards optimized for long-term retention using spaced repetition principles.

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

## Core Principles

### 1. Minimum Information Principle
Each card should test ONE atomic piece of knowledge. Break complex topics into multiple simple cards.

**Bad:** "Explain photosynthesis and its stages"
**Good:** "What is the primary product of the light-dependent reactions in photosynthesis?" → "ATP and NADPH"

### 2. Use Cloze Deletions for Definitions
For definitions and key terms, formulate as fill-in-the-blank when appropriate.

**Example:** "{{c1::Mitochondria}} are the powerhouses of the cell"

### 3. Ask Questions, Don't State Facts
Frame cards as questions that require active recall, not passive recognition.

**Bad:** "The capital of France is Paris"
**Good:** "What is the capital of France?" → "Paris"

### 4. Add Context and Cues
Include enough context to disambiguate without giving away the answer.

**Example:** "In JavaScript, what method removes the last element from an array?" → "pop()"

### 5. Use Bidirectional Cards When Appropriate
For vocabulary, terms, or reversible facts, create cards in both directions.

**Example:**
- "What is the Spanish word for 'house'?" → "casa"
- "What does 'casa' mean in English?" → "house"

### 6. Include Mnemonics and Memory Hooks
When useful, add memorable associations, acronyms, or visual cues.

**Example:** "Order of operations in math (mnemonic)" → "PEMDAS: Please Excuse My Dear Aunt Sally"

### 7. Avoid Orphan Cards
Related cards should build on each other. Create prerequisite cards for complex topics.

### 8. Image Occlusion for Visual Content
When processing images (diagrams, charts, anatomical drawings):
- Describe what should be labeled or identified
- Create cards that test recognition of specific parts
- Reference the visual elements clearly

## Card Types to Generate

1. **Basic (Front/Back):** Simple question and answer
2. **Basic (Reversed):** Creates both forward and reverse cards
3. **Cloze:** Fill-in-the-blank with `{{c1::answer}}` syntax
4. **Image-based:** Description cards for visual content

## Process for Creating Cards

1. **Analyze the content** - Identify key concepts, terms, facts, and relationships
2. **Chunk information** - Break into atomic, testable units
3. **Prioritize** - Focus on high-value, frequently-tested, or foundational knowledge
4. **Formulate questions** - Write clear, unambiguous prompts
5. **Write concise answers** - Keep answers brief and precise
6. **Add context** - Include tags or hints where helpful
7. **Review for redundancy** - Eliminate duplicate or overlapping cards

## Handling Different Content Types

### Text/Notes
Extract key facts, definitions, processes, and relationships. Focus on what's likely to be tested or practically useful.

### Images/Diagrams
- Describe visual elements that need identification
- Create cards for labels, parts, processes shown
- Reference spatial relationships ("the structure on the left side...")

### Code/Technical Content
- Test syntax, function names, and behavior
- Include code snippets in monospace formatting
- Focus on gotchas and commonly confused elements

### Language Learning
- Vocabulary with example sentences
- Grammar rules with examples
- Bidirectional translations

## Output Format Example

```
What is the capital of Japan?	Tokyo
What Japanese city was the imperial capital before Tokyo?	Kyoto
{{c1::Mitochondria}} are known as the powerhouses of the cell	(cloze card)
In Python, what function returns the length of a list?	len()
```

## Additional Resources

See [references/patterns.md](references/patterns.md) for more examples across different subjects.
