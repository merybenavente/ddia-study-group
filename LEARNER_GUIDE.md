# LEARNER_GUIDE.md — How to work in this repo

You're using Claude Code in a deliberately constrained mode. The constraints exist because the goal is to *learn* the DDIA material, not to produce a working repo. If you just wanted a working repo, you wouldn't need this scaffolding.

Here's what to expect and how to get the most out of it.

## The three phases per chapter

Each chapter runs in order: **theory → design → implementation → failure experiments → review.** Claude will not skip ahead with you. This is intentional. Each phase is a different mode of engagement with the chapter's content:

- **Theory** is conversational. Claude interviews you on the chapter and writes a short `THEORY.md` when you've shown you can articulate, apply, and self-assess on the core concepts. There is no code yet.
- **Design** is also pre-code. You write `DESIGN.md` — scenario constraints, decisions with rejected alternatives, a failure model. Claude probes your design but does not propose alternatives.
- **Implementation** is code, but in small atomic units. Claude writes one function/method/type at a time and stops. You inspect, accept, modify, or rewrite. The pauses are the point.
- **Failure experiments** are where your design's failure model gets tested against reality. *You* pick what to break, based on what you predicted. Claude implements the chaos mechanism; you observe and write up the gap between prediction and observation.
- **Review** is a separate Claude session (paste `REVIEWER_PROMPT.md`). Mechanical checks, then Socratic interrogation. It is not nice.

## What Claude will refuse to do

- Tell you the answer to a chapter concept ("explain snapshot isolation").
- Make a design decision for you.
- Write code for a function whose purpose you haven't stated.
- Add "while I'm here" improvements.
- Write more than one named unit at a time during implementation.
- Skip phases.

When Claude refuses, it will explain why in one or two sentences. **Don't argue.** You can override most refusals by insisting, but each override leaves a marker that the reviewer will find. Override sparingly and only when you genuinely have a reason.

## How to actually use this well

**Read the chapter first.** Genuinely read it. Theory phase is not a substitute for reading; it's a check on whether reading landed.

**Take the design phase seriously.** This is the part most learners want to skip. Don't. The failure experiments later are only meaningful if you predicted something specific. Vague designs produce uninformative failures.

**Don't rush implementation.** When Claude writes a function and stops, actually read it. Decide if it's right. Rewrite it if you don't like it. The friction is doing the work you came here to do.

**Be honest in the AI Collaboration Notes section.** The point of this repo (for your portfolio) is to be the *opposite* of polished-but-shallow. Documenting what you let Claude drive, what you hand-wrote, and where Claude was wrong is the part that makes the repo credible to people reading it later.

**Use the meta skill for plumbing.** Don't spend your thinking budget on `pyproject.toml`. Tell Claude to set the project up and move on.

## What "done" feels like

A chapter is done when you can sit in front of a stranger, point at your code, and explain every non-trivial decision — *and* show them the failure experiments that tested your predictions. If you can't do that, you skipped something. Go back.

## When to break the rules

These constraints exist to keep you in the learning loop. If they ever start *removing* you from it — e.g., you've actually understood a concept thoroughly and the theory interview is just churning — say so. Claude is calibrated to be strict, not infinite. "I think I'm past this, let's move on" is a legitimate move when it's true. You'll know it's true if you can defend it; you'll know it isn't if you're just impatient.
