# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This project builds a searchable unofficial student guide using RAG (Retrieval-Augmented Generation). It ingests advice documents from the campus life corpus, stores them in a vector database, and generates grounded answers with source citations while blocking off-topic queries. It answers questions about courses, parking, dining, student accounts, and other university topics. The system retrieves information from the campus-life documents and uses those documents to create an answer with a source.


## Chunking Strategy

**Chunk size:** 26
**Overlap:** 0

**Actual strategy:** one complete document per chunk; no fixed character size
and no overlap.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

I kept each short campus-life document as one chunk and used no overlap. The
documents are already short and each one keeps its topic, so splitting them
would risk separating the heading from the information that explains it.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::split_documents`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt` — produced by: `chunker.py::split_documents`

```text
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt` — produced by: `chunker.py::split_documents`

```text
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt` — produced by: `chunker.py::split_documents`

```text
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt` — produced by: `chunker.py::split_documents`

```text
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

How long does a student account stay active after graduation?

**Answer:**

Your student account stays active for six months after you graduate
(`admin_wifi_and_accounts.txt`).

**Source:** `admin_wifi_and_accounts.txt`

```
```

**My relevance cutoff:**

I kept the cutoff at **0.6**. The five in-corpus questions had best distances
from 0.198 to 0.368. The five out-of-scope questions had best distances from
0.825 to 0.934, so 0.6 sits between the two groups.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| Do dining dollars roll over from spring to the following autumn? | Yes | 0.204 |
| How quickly do student permits for the west parking lots sell out? | Yes | 0.198 |
| How long does a student account stay active after graduation? | Yes | 0.368 |
| Through which week can students drop a course? | Yes | 0.319 |
| How many hours per week should students expect to spend outside class for CS 210? | Yes | 0.278 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I used AI to understand Milestone 3 and write the chunking code. Because the campus_life documents are short, I changed split_documents() in chunker.py to keep each complete document as one chunk with no overlap, so the information stays together and sentences are not split.

**2.**  I used AI to choose five answerable questions from the corpus and give each an expects phrase. I also used AI to pressure-test the acceptance criteria so they had clear numbers or observable results and covered different parts of the system.

**3.** I used AI to compare the before and after results after changing the
chunker. It helped me notice that the number of chunks increased from 88 to
183 and that the CS 210 retrieval distance improved, but the overall pass
rates stayed the same. I kept the change and recorded that some new chunks
were only 36 characters long and may need more review.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk quality | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Correct factual answers | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Evidence from the run

Source: `results/run_2026-09-26_1809_before.md`, produced by
`run_eval.py::run_once`.

**Criterion 1 — retrieved chunks contained the answer:**

```text
Sources retrieved: admin_wifi_and_accounts.txt, admin_graduation_requirements.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt, money_jobs.txt
A student account stays active for six months after you graduate.
```

**Criterion 2 — answers named a source:**

```text
A student account stays active for six months after you graduate.
Source: admin_wifi_and_accounts.txt
```

**Criterion 3 — the gate refused out-of-scope questions:**

```text
Produced by: run_eval.py::check_out_of_scope, cutoff 0.6. Refused 5 of 5.
What is the capital of Mongolia? | 0.825 | refused
How do I change the oil in a diesel engine? | 0.934 | refused
Who won the 1994 World Cup? | 0.886 | refused
What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused
How do I write a for loop in Rust? | 0.896 | refused
```

**Criterion 4 — chunks were complete:**

```text
Source: admin_add_drop_deadline.txt
Produced by: chunker.py::split_documents
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript.
```

I checked the five sample chunks from `chunker.py::split_documents`; all five
were complete thoughts, so the result was 5/5.

**Criterion 5 — answers contained the expected phrase:**

```text
Students should expect to spend 8 to 10 hours a week outside class for CS 210.
Source: course_cs_210_workload.txt
```

The answer contains the expected phrase `8 to 10 hours`, so the scorer marked
the question as pass.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All five questions passed in all three runs. |
| 2 | Every answer names a source | MET | All five answers named at least one source. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all five out-of-scope questions. |
| 4 | Chunk quality | MET | All five sampled chunks were complete thoughts. |
| 5 | Correct factual answers | MET | All five answers contained their expected phrases in all three runs. |

### Critical check

I also argued for the opposite verdict for each criterion:

1. **Retrieved chunks contain the answer — target: 4 of 5.** The result was
     5/5 in all three runs, so this is MET. The strongest case for MISSED is
     that the scorer checks the answer text, not independently whether the
     retrieved chunk contains the answer. I checked the retrieved sources and
     found the answers in them, so I kept MET.

2. **Every answer names a source — target: 5 of 5.** The result was 5/5 in
     all three runs, so this is MET. The strongest case for MISSED is that an
     answer could name a filename without truly using that file. The criterion
     only requires a source name, and every answer included one, so MET is the
     literal result.

3. **The gate stops out-of-corpus questions — target: 4 of 5.** The gate
     refused 5/5, so this is MET. The strongest case for MISSED is that the
     out-of-scope questions were checked once rather than three times. That is
     appropriate because retrieval and the gate are deterministic, and 5/5 is
     above the target, so it remains MET.

4. **Chunk quality — target: 4 of 5.** The five sampled chunks were 5/5
     complete thoughts, so this is MET. The strongest case for MISSED is that
     five samples cannot prove that all 88 chunks are good. The target asks for
     five sampled chunks, however, and all five passed, so MET is supported.

5. **Correct factual answers — target: 4 of 5.** The result was 5/5 in all
     three runs, so this is MET. The strongest case for MISSED is that the
     scorer only checks an expected phrase and a source name; it cannot prove
     every sentence is fully grounded. For this criterion, every answer had
     the expected phrase and a source, so MET is the result.

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I did not miss any of the five criteria, so I did not find a failure in
loading, chunking, embedding, retrieval, or generation. The targets were a
little safe. My campus_life corpus has 88 short documents, averaging 317
characters, and none is longer than 800 characters. Because of that, keeping
each document as one chunk avoided sentence-splitting problems. Also, most
criteria allowed one failure out of five, and the chunk test looked at only
five samples. I would make criterion 4 stricter next time by checking all 88
chunks instead of only five.

## The Improvement

**What I changed:**

I changed `chunker.py::split_documents` from one document per chunk to
paragraph-based chunks. I kept each document heading with its first paragraph
and used no overlap.

**Why I picked it:**

The diagnosis showed that all 88 campus-life documents were already shorter
than the starter's 800-character window, so the original chunking test was
very easy. Paragraph-based chunks give retrieval smaller, more focused pieces
to search.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk quality | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Correct factual answers | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

The change helped retrieval for the CS 210 question: its best distance
improved from 0.2784 before the change to 0.2403 after it. The other questions
still passed, and the gate still refused 5 of 5 out-of-scope questions. The
overall criterion scores stayed the same at 5/5, so the improvement was useful
but did not change the final pass rates. It also created 183 chunks instead of
88, with a shortest chunk of 36 characters, so paragraph splitting may create
some chunks that are too small and should be reviewed further.

**Evidence:**

Before: `results/run_2026-09-26_1809_before.md` — 88 chunks, all five
questions passed in all three runs.

After: `results\run_2026-09-26_2033_after.md` — 183 chunks, all five
questions passed in all three runs, and the gate refused 5 of 5 out-of-scope
questions.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

None of the five criteria were missed after the improvement. However, the new
paragraph-based chunker created 183 chunks, including a shortest chunk of 36
characters. Some chunks may be too small to provide enough context, even
though the five sampled chunks passed. I stopped here because the evaluation
did not show a failed criterion, but this is the next issue I would investigate.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I would make criterion 4 stricter. Instead of checking only five sampled
chunks, I would check all 183 chunks after the improvement and require every
chunk to be a complete thought with enough context. I would also make
criterion 5 check whether the answer is fully supported by its cited document,
not only whether it contains an expected phrase.

## Capstone

**The System**

I am extending The Unofficial Guide, the existing RAG student-guide system in
this repository. It already loads campus-life documents, retrieves relevant
chunks, generates grounded answers, and exposes the pipeline through
`serve.py`.

**The Shape**

I chose **Shape A: deploy and instrument**. I will use the existing HTTP
service as a documented local deployment, start it with one command, and add
structured request logging with timestamps, questions, answers, and
end-to-end latency. I will also measure the cost of a run using the model
usage data already reported by the generation layer.

**Out of Scope**

I am not adding a second retrieval strategy, changing the chunking strategy,
or rebuilding the command-line or web interface. I will focus only on making
the existing run path reproducible and making its behavior and cost visible
after a session.

**Milestone 3 — Run Path**

I chose the local-with-logs path. From a clean checkout, the service is started
with `python serve.py` after the one-time `python app.py index` command. The
environment needs Python 3.11–3.13, the dependencies in `requirements.txt`, a
local `.env` containing `GEMINI_API_KEY`, and the bundled embedding model,
which downloads during the first index run. The complete Windows Command
Prompt procedure is in `RUNNING.md`.

**Instrumentation**

Each `/ask` request writes one JSON record to
`results/service_runs.jsonl`. Records include the UTC timestamp, question,
answer or error, HTTP status, latency in milliseconds, refusal status, sources,
and per-request prompt/output/total token usage. The invalid-input request is
included to show that failures are logged too.

The following ten successful records and one rejected-input record came from
the main local service run on 2026-11-15. Each line is one JSON record from
`results/service_runs.jsonl`:

```json
{"timestamp":"2026-11-15T21:17:47.131262+00:00","endpoint":"/ask","question":"How long does a student account stay active after graduation?","answer":"A student account stays active for six months after you graduate (admin_wifi_and_accounts.txt).","status_code":200,"latency_ms":6303.5,"refused":false,"sources":["admin_graduation_requirements.txt","admin_pass_fail_option.txt","admin_wifi_and_accounts.txt","advising_registration.txt","money_jobs.txt"],"best_distance":0.3678,"threshold":0.6,"token_usage":{"prompt":411,"output":22,"total":433}}
{"timestamp":"2026-11-15T21:17:55.889556+00:00","endpoint":"/ask","question":"What is the capital of Mongolia?","answer":"I don't have enough information about that.","status_code":200,"latency_ms":72.1,"refused":true,"sources":[],"best_distance":0.7873,"threshold":0.6,"token_usage":{"prompt":0,"output":0,"total":0}}
{"timestamp":"2026-11-15T22:35:00.129242+00:00","endpoint":"/ask","question":"Do dining dollars roll over from spring to the following autumn?","answer":"No, dining dollars do not roll over from spring to the following autumn; whatever is left in May disappears. (Source: admin_dining_dollars.txt)","status_code":200,"latency_ms":12171.89,"refused":false,"sources":["admin_dining_dollars.txt","admin_meal_plan_changes.txt","dining_halden_hall.txt","dining_north_kitchen.txt","dining_pellew_dining_hall.txt"],"best_distance":0.2037,"threshold":0.6,"token_usage":{"prompt":379,"output":33,"total":412}}
{"timestamp":"2026-11-15T22:35:01.527038+00:00","endpoint":"/ask","question":"How quickly do student permits for the west parking lots sell out?","answer":"Student permits for the west lots sell out in about three days. (Source: admin_parking_permits.txt)","status_code":200,"latency_ms":1061.26,"refused":false,"sources":["admin_parking_permits.txt","advising_registration.txt","course_cs_210.txt","course_econ_101.txt","course_stat_150.txt"],"best_distance":0.1975,"threshold":0.6,"token_usage":{"prompt":321,"output":25,"total":346}}
{"timestamp":"2026-11-15T22:35:01.674782+00:00","endpoint":"/ask","question":"How long does a student account stay active after graduation?","answer":"A student account stays active for six months after you graduate (admin_wifi_and_accounts.txt).","status_code":200,"latency_ms":102.72,"refused":false,"sources":["admin_graduation_requirements.txt","admin_pass_fail_option.txt","admin_wifi_and_accounts.txt","advising_registration.txt","money_jobs.txt"],"best_distance":0.3678,"threshold":0.6,"token_usage":{"prompt":0,"output":0,"total":0}}
{"timestamp":"2026-11-15T22:35:02.307515+00:00","endpoint":"/ask","question":"Through which week can students drop a course?","answer":"Students can drop a course through the end of week six. (Source: admin_add_drop_deadline.txt)","status_code":200,"latency_ms":608.98,"refused":false,"sources":["admin_add_drop_deadline.txt","admin_pass_fail_option.txt","advising_registration.txt","course_biol_160.txt","money_jobs.txt"],"best_distance":0.3189,"threshold":0.6,"token_usage":{"prompt":390,"output":25,"total":415}}
{"timestamp":"2026-11-15T22:35:03.167765+00:00","endpoint":"/ask","question":"How many hours per week should students expect to spend outside class for CS 210?","answer":"Students should expect to spend 8 to 10 hours a week outside class for CS 210. \n\nSources: `course_cs_210.txt` and `course_cs_210_workload.txt`","status_code":200,"latency_ms":837.06,"refused":false,"sources":["course_cs_210.txt","course_cs_210_workload.txt","course_econ_101.txt","course_stat_150.txt","course_stat_150_workload.txt"],"best_distance":0.2403,"threshold":0.6,"token_usage":{"prompt":318,"output":53,"total":371}}
{"timestamp":"2026-11-15T22:35:04.199299+00:00","endpoint":"/ask","question":"What is the housing lottery like?","answer":"Based on the housing lottery, rising sophomores receive a randomly drawn number, while juniors and seniors are ordered by accumulated credit hours first, with a random tie-break. Numbers are released the second week of March, and selection takes place over four evenings. \n\nSource: admin_housing_lottery.txt","status_code":200,"latency_ms":970.55,"refused":false,"sources":["admin_housing_lottery.txt","advising_registration.txt","housing_aldridge_hall.txt","housing_morrow_house.txt"],"best_distance":0.3443,"threshold":0.6,"token_usage":{"prompt":390,"output":63,"total":453}}
{"timestamp":"2026-11-15T22:35:05.124858+00:00","endpoint":"/ask","question":"What are the laundry costs in Innisfree Hall?","answer":"In Innisfree Hall, laundry costs $1.75 for a wash and $1.75 for a dry. \n\nSources: housing_innisfree_hall_laundry.txt and housing_innisfree_hall.txt","status_code":200,"latency_ms":901.44,"refused":false,"sources":["housing_aldridge_hall.txt","housing_innisfree_hall.txt","housing_innisfree_hall_laundry.txt","housing_morrow_house.txt","housing_old_brewhouse.txt"],"best_distance":0.2454,"threshold":0.6,"token_usage":{"prompt":407,"output":52,"total":459}}
{"timestamp":"2026-11-15T22:35:06.030623+00:00","endpoint":"/ask","question":"When should I arrive at Pellew Dining Hall to avoid the peak wait?","answer":"To avoid the peak wait at Pellew Dining Hall, you should go before 11:45 (`dining_pellew_dining_hall_followup.txt` and `dining_pellew_dining_hall.txt`).","status_code":200,"latency_ms":879.51,"refused":false,"sources":["dining_halden_hall.txt","dining_halden_hall_followup.txt","dining_pellew_dining_hall.txt","dining_pellew_dining_hall_followup.txt","dining_the_ridgeway_cafe_followup.txt"],"best_distance":0.1644,"threshold":0.6,"token_usage":{"prompt":559,"output":51,"total":610}}
```

The required failed run is the rejected empty-question request:

```json
{"timestamp":"2026-11-15T22:35:08.464528+00:00","endpoint":"/ask","question":"","answer":null,"status_code":400,"latency_ms":0.1,"refused":false,"sources":[],"token_usage":{"prompt":0,"output":0,"total":0}}
```

**What It Costs**

I measured cost as model tokens because the generation service reports actual
prompt and output token counts. For the ten records above, the
`token_usage.total` values sum to **3,499 tokens**, so the measured average is
**349.9 tokens per request** (3,499 / 10). The invalid request used zero model
tokens because it was rejected before retrieval and generation.

```text
Ten-request total tokens: 3,499
Average tokens per request: 3,499 / 10 = 349.9
Measurement method: sum token_usage.total from ten service_runs.jsonl records
and divide by ten.
```

**Run Log and Verdicts**

I ran the five Capstone criteria three separate times against the local
`serve.py::ask` endpoint. Each trial sent 10 valid requests and 3 empty
requests. The source records are in
`results/service_runs.jsonl`; the three trials are the final 39 records.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Every request is recorded | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Records contain required evidence | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 3. Invalid input is handled and logged | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Normal request latency stays bounded | 9 of 10 under 15s | 10/10 | 10/10 | 10/10 | MET |
| 5. Token use stays measurable and bounded | average <= 500 | 412.8 | 409.4 | 406.3 | MET |

Evidence extracted from `results/service_runs.jsonl`:

```text
Produced by: serve.py::ask
Run 1 valid request totals: 434, 0, 431, 432, 476, 377, 457, 469, 602, 450
Run 1 latency_ms: 3517.75, 91.31, 1152.69, 780.92, 726.44, 844.86, 2385.19, 758.67, 743.21, 722.11
Run 1 invalid requests: status_code=400, status_code=400, status_code=400

Run 2 valid request totals: 434, 0, 416, 429, 473, 377, 456, 459, 600, 450
Run 2 latency_ms: 737.13, 81.24, 631.93, 726.36, 1344.63, 657.52, 734.09, 735.49, 650.41, 638.12
Run 2 invalid requests: status_code=400, status_code=400, status_code=400

Run 3 valid request totals: 441, 0, 426, 429, 417, 377, 455, 470, 603, 445
Run 3 latency_ms: 1366.90, 95.28, 676.21, 738.47, 656.01, 724.71, 723.91, 886.39, 1032.31, 1249.97
Run 3 invalid requests: status_code=400, status_code=400, status_code=400
```

All three runs met the targets. No diagnosis was needed for a missed
criterion. The slowest valid request was 3,517.75 ms, below the 15-second
limit, and all invalid requests were recorded with HTTP 400.
