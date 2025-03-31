# Evaluation Criteria

## Introduction

To systematically assess the effectiveness of the prompts developed for the virtual project management consultant, I've established a comprehensive set of evaluation criteria. These criteria will be used to measure the quality of ChatGPT's responses and guide further refinements.

## Core Evaluation Dimensions

The evaluation framework consists of six core dimensions, each with specific criteria and measurement approaches:

### 1. Relevance & Specificity

**Key Question**: How well does the response address the specific project management scenario and context provided?

**Criteria**:
- **Contextual Adaptation**: Degree to which the response incorporates and adapts to the context parameters provided (project type, team composition, methodology, etc.)
- **Domain Specificity**: Use of domain-appropriate language, concepts, and examples relevant to project management
- **Scenario Alignment**: Focus on addressing the specific scenario rather than generic project management advice
- **Parameter Responsiveness**: Variation in response based on changes to context parameters

**Measurement Approach**:
- 5-point scale for each criterion (1=Poor, 5=Excellent)
- Identify specific instances of contextual elements being incorporated
- Compare responses across different parameter settings

### 2. Comprehensiveness & Structure

**Key Question**: Does the response cover all requested elements in a well-organized manner?

**Criteria**:
- **Component Coverage**: Inclusion of all requested components in the prompt
- **Organizational Clarity**: Logical flow and clear structure using headings, lists, etc.
- **Depth Balance**: Appropriate allocation of depth to different components based on importance
- **Information Hierarchy**: Effective prioritization of information from most to least important

**Measurement Approach**:
- Checklist of requested components (all/most/some/few)
- Assessment of organizational elements (headings, sections, lists)
- Proportion of content devoted to each component

### 3. Actionability & Practicality

**Key Question**: How immediately useful and implementable is the advice provided?

**Criteria**:
- **Implementation Guidance**: Clear steps for putting advice into practice
- **Resource Consideration**: Acknowledgment of realistic resource constraints
- **Immediate Applicability**: Inclusion of actions that can be taken immediately
- **Tool & Template Provision**: Specific tools, templates, or frameworks provided

**Measurement Approach**:
- Count of actionable steps provided
- Assessment of resource realism (high/medium/low)
- Identification of immediate vs. long-term actions
- Count and quality of tools/templates included

### 4. Expertise & Credibility

**Key Question**: Does the response demonstrate project management expertise and provide credible guidance?

**Criteria**:
- **Best Practice Alignment**: Consistency with established project management best practices
- **Methodology Accuracy**: Correct representation of methodologies mentioned
- **Reasoning Transparency**: Clear rationale provided for recommendations
- **Authority Markers**: Inclusion of elements that demonstrate expertise (statistics, research references, experience-based insights)

**Measurement Approach**:
- Expert review of best practice alignment (high/medium/low)
- Identification of methodology misrepresentations
- Count of explained rationales vs. unsupported assertions
- Presence of authoritative elements

### 5. Adaptability & Flexibility

**Key Question**: How well does the response acknowledge variation and provide adaptable guidance?

**Criteria**:
- **Contingency Consideration**: Acknowledgment of different scenarios or outcomes
- **Scalability Guidance**: Advice on how to scale approaches for different project sizes
- **Methodology Flexibility**: Adaptation of advice for different project methodologies
- **Constraint Adaptability**: Options for adapting advice under different constraints

**Measurement Approach**:
- Count of contingency scenarios addressed
- Presence of scaling guidance (yes/limited/no)
- Assessment of methodology-specific variations
- Range of constraint adaptations provided

### 6. Engagement & Clarity

**Key Question**: How clear, engaging, and usable is the response?

**Criteria**:
- **Language Clarity**: Use of clear, jargon-appropriate language
- **Engagement Elements**: Inclusion of engaging elements (examples, analogies, visualizations)
- **Instructional Quality**: Effectiveness of explanations and instructions
- **Cognitive Accessibility**: Appropriate complexity level for the intended audience

**Measurement Approach**:
- Readability metrics (Flesch-Kincaid)
- Count of engaging elements
- User comprehension assessment
- Complexity analysis (sentence length, technical term frequency)

## Scoring System

Each prompt response will be evaluated using a combination of:

1. **Criterion Scores**: 1-5 rating for applicable criteria (1=Poor, 5=Excellent)
2. **Dimension Scores**: Average of criterion scores within each dimension
3. **Overall Effectiveness Score**: Weighted average of dimension scores
4. **Qualitative Assessment**: Narrative evaluation of strengths and weaknesses

## Weighting Framework

Dimensions will be weighted based on their importance to the project management context:

- Relevance & Specificity: 25%
- Actionability & Practicality: 25%
- Comprehensiveness & Structure: 20%
- Expertise & Credibility: 15%
- Adaptability & Flexibility: 10%
- Engagement & Clarity: 5%

## Evaluation Process

The evaluation process will include:

1. **Systematic Testing**: Running each prompt multiple times with different parameters
2. **Blind Comparison**: Comparing responses from different prompt versions without knowing which is which
3. **User Validation**: Having actual project managers review and assess responses
4. **Improvement Tracking**: Monitoring scores across prompt iterations to measure improvement

## Success Thresholds

The following thresholds will determine the success of a prompt:

- **Excellent**: Overall score ≥ 4.5, no dimension below 4.0
- **Good**: Overall score ≥ 4.0, no dimension below 3.5
- **Acceptable**: Overall score ≥ 3.5, no dimension below 3.0
- **Needs Improvement**: Overall score < 3.5 or any dimension below 3.0

## Evaluation Scenarios

To ensure comprehensive assessment, each prompt will be tested using multiple parameter combinations:

### Project Type Variations
- Software development project
- Construction project
- Marketing campaign
- Product development
- Business process improvement

### Team Configuration Variations
- Small co-located team (3-5 people)
- Medium-sized hybrid team (8-12 people)
- Large distributed team (15+ people across multiple locations)
- Cross-functional team with diverse expertise
- Team with mostly junior members

### Methodology Variations
- Traditional Waterfall
- Agile/Scrum
- Hybrid approach
- Critical Path Method
- PRINCE2

### Project Constraint Variations
- Tight timeline, adequate resources
- Adequate timeline, limited budget
- High complexity, strategic importance
- Regulatory/compliance requirements
- Multiple stakeholders with competing priorities

## User Testing Plan

The evaluation will include feedback from actual project managers with diverse backgrounds:

1. **Participant Selection**: Recruit 8-10 project managers with varied:
   - Experience levels (junior, mid-level, senior)
   - Industry backgrounds
   - Methodological preferences

2. **Test Protocol**:
   - Provide participants with specific project scenarios
   - Have them use the prompts to interact with ChatGPT
   - Ask them to evaluate the response quality using a simplified version of the evaluation criteria
   - Conduct follow-up interviews to gather qualitative feedback

3. **User Evaluation Metrics**:
   - Perceived usefulness (1-5 scale)
   - Implementation likelihood (1-5 scale)
   - Relevance to their specific context (1-5 scale)
   - Comparison to standard ChatGPT responses without optimized prompts

## Continuous Improvement Framework

The evaluation results will feed into a continuous improvement process:

1. **Gap Analysis**: Identifying dimensions with the lowest scores
2. **Root Cause Analysis**: Determining why certain criteria are not being met
3. **Targeted Refinement**: Modifying prompts to address specific weaknesses
4. **Iteration Testing**: Re-testing refined prompts to measure improvement
5. **Cross-Prompt Learning**: Applying successful elements from high-scoring prompts to others

## Documentation of Evaluation Results

For each prompt evaluation, I will document:

1. **Parameter Combinations Tested**: The specific context variables used
2. **Dimension Scores**: Ratings for each of the six dimensions
3. **Overall Score**: The weighted effectiveness rating
4. **Key Strengths**: Specific aspects of the response that were particularly effective
5. **Improvement Opportunities**: Areas where the response could be enhanced
6. **Iteration Comparison**: How the current version compares to previous iterations
7. **User Feedback**: Comments and ratings from project manager testers

## Conclusion

This comprehensive evaluation framework provides a systematic approach to assessing and improving the quality of the virtual project management consultant prompts. By applying these criteria consistently across all prompts and iterations, I can ensure that the final prompts generate the most practical, relevant, and actionable project management advice possible.

The framework balances quantitative measurement with qualitative assessment, ensuring both objective evaluation and contextual understanding of prompt effectiveness. The prioritization of relevance and actionability reflects the primary goal of creating a virtual consultant that provides genuinely helpful project management guidance.