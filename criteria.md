# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

My five questions cover different documents and topics in the campus-life corpus. Four out of five allows one difficult retrieval while still requiring the system to work for most questions.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

The system keeps the source filename with each document, so every answer should identify the document that provided its information.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

The five out-of-scope questions are unrelated to campus life, so the gate should refuse most of them instead of generating unsupported answers. Four out of five allows one possible error.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

At least 4 of 5 sampled chunks should contain complete thoughts and not cut a sentence in half.



**Why this target:**

The campus-life documents are short and usually contain one complete topic, so the chunks should preserve complete information.


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**

At least 4 of 5 generated answers should contain the expected phrase from `questions.py`.

Each question has a specific factual answer, such as "six months" or "week six," so the expected phrase gives a clear way to check correctness.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone acceptance criteria

These criteria apply to the Shape A extension: local deployment and structured
instrumentation for the HTTP service. They are separate from the Unit 1
criteria above.

## 1. Every request is recorded

For 10 of 10 `/ask` requests, `results/service_runs.jsonl` contains exactly
one new JSON record.

**Why this target:

The purpose of the extension is to make the running service observable. A
missing record would make one request impossible to diagnose after the fact, so
the target is 10 of 10 rather than allowing an unrecorded request.

## 2. Records contain the required evidence

For 10 of 10 logged `/ask` requests, the record contains a timestamp, question,
answer or error, HTTP status, and non-negative `latency_ms` value.

**Why this target:

These fields describe what came in, what came out, whether the request
succeeded, and how long it took. Requiring all 10 records prevents a partial
logger from appearing complete.

## 3. Invalid input is handled and logged

For 3 of 3 requests with an empty question, the service returns HTTP 400 and
writes a record with `status_code` 400 and an empty `question`.

**Why this target:

An empty request is a simple failure a user can trigger without damaging the
service. Three repeated trials show that failure handling is consistent, not a
one-time result.

## 4. Normal request latency stays bounded

At least 9 of 10 valid `/ask` requests finish in 15 seconds or less, measured
by the logged `latency_ms` value.

**Why this target:

The service uses a local embedding model and a hosted generation call. Fifteen
seconds allows for normal model and network variation while still catching a
request that hangs or becomes impractical for an interactive guide.

## 5. Token use stays measurable and bounded

The average `token_usage.total` across 10 valid `/ask` requests is no more than
500 tokens per request.

**Why this target:

The service sends retrieved context to the generation model, so larger
retrieval prompts increase measured usage. A 500-token average leaves room for
the five retrieved chunks while detecting an unexpectedly large prompt or
answer.
