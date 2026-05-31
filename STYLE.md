# Writing style for this course

Synthesized from how the best dev-education sites actually write (Josh Comeau, Julia Evans,
MDN, Real Python, freeCodeCamp, The Odin Project, Stripe docs, fast.ai). This is the voice
every doc and lesson here should use. If you edit a page, match it.

## Voice in one line
Write like a competent friend at a whiteboard. Talk to one reader: a senior DevOps engineer
who's new to LLMs. Respect what she already knows; explain only what's actually new.

## Do
- Use "you" for the reader, "we" when we walk through steps together. Save "I" for a real
  opinion or a real admission ("I had to look this up too").
- Present tense, active voice, contractions on.
- Lead with the concrete: a working line of code, a real error, a plain analogy. Theory after.
- Vary sentence length. A short one lands. Use it after a long one.
- Name the gotcha out loud, often as a question heading ("Why max_iterations and not a while True?").
- Be honest about tradeoffs and danger. Say when something costs money or can loop forever.
- Bold at most one phrase per paragraph. Often none.
- End a section by pointing forward, not by summarizing what you just said.

## Don't (the AI-slop tells we're removing)
- No em-dash on every line. One per few paragraphs, max. Prefer a period, colon, or parens.
- No "it's not just X, it's Y." No "Here's the thing." No "in today's fast-paced world."
- No hype words: cheat code, unlock, supercharge, leverage, harness, seamless, robust,
  powerful, game-changer, revolutionize.
- Don't force every list into three items. Use the number that's true.
- No empty transitions ("Now that we understand the basics, let's move on...").
- No hollow outros ("By mastering this, you'll be well on your way..."). Cut them.
- Don't say "simply / just / obviously" before a hard step.
- Don't bold half a sentence. Don't title-case headings. Sentence case only.

## Two fast tests when editing
1. Delete a sentence. If the meaning survives, it was filler.
2. For any group of three, delete the third. If nothing's lost, it was rhythm, not content.

## Before / after
- AI-ish: "In today's landscape, tool calling is a powerful primitive that unlocks robust,
  scalable agents." → Plain: "Tool calling is how a model asks your code to do something.
  It's the one mechanism every agent is built on."
- AI-ish: "Your DevOps background is a cheat code that gives you an unfair advantage." →
  Plain: "You've already done the hard part of this job, just for normal services: deploys,
  monitoring, rollbacks. Agents need the same things."
