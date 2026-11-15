# Record of AI assistance

*This file was originally written in Turkish by the student. It was translated into English in November 2026 without changing its content. The final section, "Review session", was added at that time.*

# Week 1: Elementary Cellular Automata

In this week's `01_elementary_CA.ipynb` work I received support from Claude and ChatGPT to understand some technical topics and to check results.

## Help I received from AI

- I received explanations to understand the bit shift (`>>`) and bit mask (`&`) operations in the `rule_output` function.
- I received help understanding the logic of the ordering in the Rule 110 table.
- I checked some values and results in the observation table.
- I received ideas and explanations for the investigation of Rule 90 and the formula $N_1(t) = 2^{\text{popcount}_2(t)}$.

## My own work

- I completed the functions in the assignment myself.
- I studied how the code and the rules work.
- I compared the patterns produced by different rules.
- I tried to understand the relationship between bit operations and Rule 90.

## Note

I used AI especially to learn technical topics I did not understand and to check some results. I tried to understand the logic of the code myself.


# Week 2: Rule Classification

In this week's `02_rule_classification.ipynb` work I received support from AI to check some code and to understand technical topics.

## Help I received from AI

- I received explanations of how some functions work.
- I received coding support in the section where the 256 rules are examined and in the density and activity calculations.
- I received help preparing the plots and fixing some code errors.
- I received ideas when evaluating the results for the 16 selected rules.

## My own work

- I checked the tests and the results in the notebook.
- I studied the concepts of density and activity.
- I compared the behaviours in the plots.
- I tried to understand Wolfram's four classes and the effect of initial conditions.

## Note

I used AI mostly for technical explanations and code checking. I did not change the tests or tune the results to predetermined values. I evaluated the classifications by comparing them with the plots and the numerical results.


# Week 3: Sensitivity to Initial Conditions

In this week's `03_sensitivity.ipynb` work I received support from Claude especially when rebuilding some code and interpreting results.

## Help I received from AI

- I received code suggestions when rebuilding the four TODO functions.
- I received support in running the experiments and organising the numerical results.
- I received help writing some tables and explanations more clearly.
- I received ideas when interpreting the results in the plots.

## My own work

- I tried to understand how the functions work.
- I studied the concepts of Hamming distance and perturbation radius.
- I compared how initial changes spread in different rules.
- I planned to check the code and the results again and to ask about points I did not understand in the meeting.

## Note

I used AI especially to check code, to learn the topic and to understand the results. I tried to go over the work again so that I could explain its logic on my own.


# Week 4: Conway's Game of Life

In some parts of this week's `04_game_of_life.ipynb` work I received support from Claude.

## Help I received from AI

- I received code suggestions in some TODO functions where I got stuck.
- I used ideas and suggested answers for the written questions.
- I received support when checking that the code works and checking the test results.

## My own work

- I placed the code in the notebook and ran it in Google Colab.
- I studied `np.roll`, Boolean masks and the B3/S23 rules.
- I compared the still life, oscillator and spaceship examples.
- I tried to understand the logic of the code and of the results obtained.

## Note

I used AI as a helping tool especially where I got stuck. I ran the notebook myself and checked the results.


# Week 5: Random Initial Conditions

In some parts of this week's `05_random_initial_conditions.ipynb` work I received support from AI.

## Help I received from AI

- I received code suggestions in a few TODO parts where I got stuck.
- I used it to get ideas for some written questions.
- I received support when checking that the code works.
- I received help in preparing the additional experiments and comparing the results.

## My own work

- I ran the notebook myself in Google Colab.
- I checked the tests and the results.
- I examined the results in the plots.
- I tried to understand the concepts of density, activity and standard deviation.
- I compared the values M = 100 and 300, the parameter q and different grid sizes.

## Note

I used AI as a helping tool where I got stuck and when preparing the additional experiments. I examined the results and tried to understand them.


# Week 6: Stochastic Game of Life

In some parts of this week's `06_stochastic_life.ipynb` work I received support from AI.

## Help I received from AI

- I received code suggestions in some TODO parts where I got stuck.
- I received support when preparing the code for the independent and clustered death models.
- I received help running the 480 simulations and speeding up the process.
- I received support in preparing the plots and checking the code.

## My own work

- I studied the effects of the random death probability on the system.
- I worked on the idea of comparing independent and clustered deaths.
- I chose the values of L as 60, 80, 100 and 200.
- I increased the experiments to 3,000 steps to see longer-term results.
- I tried to understand density, activity and extinction times and to interpret the results.

## Note

I used AI especially where I got stuck in the code and where I needed to run many simulations. I tried to understand the logic of the experiments and the results obtained.

*[Translation note: the Week 5 entry mentions "M = 100 and 300". The notebook itself compares M = 12 and M = 24 (Section 15.1). The text was translated as written.]*


# Review session (November 2026)

This section was written during a review session with Claude (Anthropic, model Claude Opus 5.5) acting on the student's written request. It records what the AI did so that a reader, a supervisor or a journal can judge the extent of AI involvement.

## What the AI did

- Translated all Markdown text, comments, printed messages and plot labels of the six notebooks from Turkish into English. The code logic was not changed except for one variable rename in notebook 06 (see `VALIDATION_REPORT.md`, Section 3.1).
- Added visible review notes and two corrections (toad population, broken table and equation markup) to the notebooks.
- Re-executed all notebooks and compared every printed number with the stored outputs.
- Wrote the code in `analysis/` (an independent simulation engine, tests, Experiments A to F, figures and cross-checks), ran about 11,500 additional simulations and wrote the CSV files in `results/`.
- Wrote `README.md`, `VALIDATION_REPORT.md`, `CHANGELOG.md`, `requirements.txt` and the technical report in `report/`.

## What the AI did not do

- It did not change the scientific model, the original parameters or any stored result.
- It did not submit, publish, or send anything to anyone.

## Note for any future journal submission

The technical report in `report/` was drafted by an AI and is intended for review by the supervisor. If the work is later submitted to a journal whose policy restricts AI-written manuscript text (for example the National High School Journal of Science), the manuscript must be written by the student in line with that policy. AI-generated prose from this repository should not be reused or paraphrased for such a submission.
