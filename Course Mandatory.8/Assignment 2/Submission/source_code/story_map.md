# Interactive Story Map

This document provides a visual representation of our interactive narrative structure, showing primary decision points, major branches, and possible endings. This map serves as both planning tool and reference guide throughout development.

## High-Level Structure

```
                                     OPENING SCENE
                                           |
                          ┌────────────────┼────────────────┐
                          |                |                |
                     DECISION 1       DECISION 1       DECISION 1
                     (Option A)       (Option B)       (Option C)
                          |                |                |
                    PRIMARY PATH A    PRIMARY PATH B   PRIMARY PATH C
                          |                |                |
        ┌─────────────────┤        ┌───────┼────────┐      |
        |                 |        |       |        |      |
   DECISION 2        DECISION 2    |  DECISION 2    |   DECISION 2
   (Option A)        (Option B)    |  (Options)     |   (Options)
        |                 |        |       |        |      |
        |                 |        |       |        |      |
SUB-PATH A1         SUB-PATH A2    |  SUB-PATH B    |  SUB-PATH C
        |                 |        |       |        |      |
        |                 |    CONVERGENCE POINT    |      |
        |                 |            |            |      |
        |                 |        DECISION 3       |      |
        |                 |        (Options)        |      |
        |                 |            |            |      |
        |                 |      FINAL BRANCHES     |      |
        |                 |            |            |      |
    ENDING 1          ENDING 2     ENDING 3     ENDING 4  ENDING 5
```

## Path Tracking Matrix

| Decision 1 | Decision 2 | Decision 3 | Leads To   | Ending Type    |
|------------|------------|------------|------------|----------------|
| Option A   | Option A   | -          | Ending 1   | "Sacrifice"    |
| Option A   | Option B   | -          | Ending 2   | "Compromise"   |
| Option B   | Any        | Option A   | Ending 3   | "Discovery"    |
| Option B   | Any        | Option B   | Ending 4   | "Connection"   |
| Option C   | Any        | -          | Ending 5   | "Transformation"|

## Detailed Branch Map

### Opening Scene: [Brief Description]
Introduction to protagonist and initial situation

### Decision Point 1: [Central Question]
- **Option A**: [Brief Description] → PRIMARY PATH A
- **Option B**: [Brief Description] → PRIMARY PATH B
- **Option C**: [Brief Description] → PRIMARY PATH C

### PRIMARY PATH A: [Thematic Focus]
Narrative explores [specific thematic element]

#### Path A Decision Point 2: [Central Question]
- **Option A**: [Brief Description] → SUB-PATH A1
- **Option B**: [Brief Description] → SUB-PATH A2

#### SUB-PATH A1: [Brief Description]
- Key scene: [Description]
- Key character interaction: [Description]
- Development: [How this path unfolds]
- Leads to: Ending 1

#### SUB-PATH A2: [Brief Description]
- Key scene: [Description]
- Key character interaction: [Description]
- Development: [How this path unfolds]
- Leads to: Ending 2

### PRIMARY PATH B: [Thematic Focus]
Narrative explores [specific thematic element]

#### Path B Decision Point 2: [Central Question]
- Multiple options leading to variations within Path B

#### SUB-PATH B: [Brief Description]
- Key scenes and developments
- Leads to: Convergence Point

### PRIMARY PATH C: [Thematic Focus]
Narrative explores [specific thematic element]

#### Path C Decision Point 2: [Central Question]
- Options and developments
- Leads to: Ending 5

### CONVERGENCE POINT: [Situation Description]
Paths B and optional others reconverge here for narrative manageability

#### Convergence Decision Point 3: [Central Question]
- **Option A**: [Brief Description] → Leads to Ending 3
- **Option B**: [Brief Description] → Leads to Ending 4

## Ending Descriptions

### Ending 1: "Sacrifice Ending"
- **Emotional Tone**: [Description]
- **Thematic Resolution**: [How central theme is addressed]
- **Character Resolution**: [Protagonist's final state]
- **Conditions**: Reached by following Path A1

### Ending 2: "Compromise Ending"
- **Emotional Tone**: [Description]
- **Thematic Resolution**: [How central theme is addressed]
- **Character Resolution**: [Protagonist's final state]
- **Conditions**: Reached by following Path A2

### Ending 3: "Discovery Ending"
- **Emotional Tone**: [Description]
- **Thematic Resolution**: [How central theme is addressed]
- **Character Resolution**: [Protagonist's final state]
- **Conditions**: Reached by following Path B and choosing Option A at Decision 3

### Ending 4: "Connection Ending"
- **Emotional Tone**: [Description]
- **Thematic Resolution**: [How central theme is addressed]
- **Character Resolution**: [Protagonist's final state]
- **Conditions**: Reached by following Path B and choosing Option B at Decision 3

### Ending 5: "Transformation Ending"
- **Emotional Tone**: [Description]
- **Thematic Resolution**: [How central theme is addressed]
- **Character Resolution**: [Protagonist's final state]
- **Conditions**: Reached by following Path C

## Key Story Beats Across All Paths

Regardless of choices made, these elements appear in all story versions:
1. Introduction of [key character/concept]
2. Revelation about [central story element]
3. Confrontation with [major obstacle]
4. Decision regarding [core thematic question]
5. Resolution of [primary narrative tension]

## Minor Variation Points

Beyond major branches, these moments create smaller variations:
- Character interaction with [supporting character]
- Approach to [specific challenge]
- Discovery of [optional information]
- Response to [emotional moment]

## Implementation Notes

When developing specific paths through ChatGPT prompts:
1. Refer to this map to maintain awareness of overall structure
2. Specify which path is being developed in each prompt
3. Ensure consistency with events established for that path
4. Reference relevant previous choices when developing later sections
5. Maintain thematic consistency while allowing for different expressions

This story map serves as a living document that will evolve as the interactive narrative develops, ensuring coherence across the branching storylines.