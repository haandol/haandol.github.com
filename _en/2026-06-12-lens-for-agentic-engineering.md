---
layout: post
title: "A Lens for Interpreting Phenomena—and Agentic Engineering"
excerpt: Why HITL removal is my lens for agentic engineering
author: haandol
email: ldg55d@gmail.com
tags: ai agent agentic-development hitl agent-centered forward-deployed-engineer
publish: true
lang: en
date: 2026-06-12 00:00:00 +0900
translation_key: lens-for-agentic-engineering
korean_url: /2026/06/12/lens-for-agentic-engineering.html
permalink: /en/2026/06/12/lens-for-agentic-engineering.html
---

## TL;DR

- A lens makes a phenomenon predictable by holding countless variables constant according to its purpose, and I view agentic engineering through the lens of **removing humans from the loop**.

## 1. What is a lens?

Economics often uses modeling to explain economic phenomena. To bring a subject made of countless variables down to a level we can understand, modeling **holds every variable constant except the part being explained**.

We can find this way of thinking all around us.

MBTI is a familiar example.

The idea of understanding a person through four variables in their decision-making flow and sixteen types has kept it in use across many settings for quite a long time. Another example that has been my favorite for several years is Kent Beck's 3X model.

It explains every business and product through three stages—Explore, Expand, and Extract—and proposes running the organization with a strategy suited to each one.[^5]

I call the act of interpreting a phenomenon by selecting its many variables for a purpose and fixing most of them as constants a **lens**.

{% raw %}
```mermaid
flowchart LR
    subgraph V["A phenomenon made of countless variables"]
        v1["Variable"]
        v2["Variable"]
        v3["Variable"]
        v4["Variable"]
        v5["Variable"]
    end
    V --> LENS{{"Lens<br/>(vary only what must be explained,<br/>hold the rest constant)"}}
    LENS --> P["Understandable · predictable model"]
```
{% endraw %}

Having a lens or not makes a striking difference when trying to predict what lies ahead.

It is especially helpful for adjusting the next prediction after one turns out to be wrong.
Without a lens, there is little to do except guess. With a lens, **the variables held constant are explicit, so we can retrace where the prediction went wrong.** Even a failed prediction becomes material for refining the lens.

## 2. Viewing agentic engineering through the HITL lens

There are countless lenses through which to interpret a phenomenon, and the same is true for the currently popular field of agentic engineering. There may be a cost lens, a UX lens, or a lens based on competition within the ecosystem.

Personally, I often use the **HITL lens** when looking at agentic engineering. In other words, I choose to *interpret all agentic engineering using human in the loop as the criterion, especially the direction of removing it*.

The reason I chose this lens over others is simple. **It explains the development so far with the fewest exceptions and also makes the direction ahead easy to explain.** I especially like it because I think Anthropic's moves can be explained through this lens.[^1]

In this post, I will call the perspective that seeks to remove humans from the loop **agent-centered**, and its opposite **human-centered**.

## 3. Using the HITL lens to relieve agent motion sickness

I think the hypersensitive reactions people have recently shown toward AI are a kind of **motion sickness** caused by interpreting agent-centered technology from a human-centered perspective.

From a human-centered perspective, experience tells us that we should not be moving this fast, so we unconsciously keep reaching for the brakes, whether emotionally or through our actions.

But agent technology is advancing too quickly and its effects are too disruptive for those brakes to work as expected, making it difficult to keep our thinking synchronized with what is happening.

The software development life cycle turns business requirements into code. In short, it is the compilation process for business requirements.[^4]

Agentic engineering pushes this process in an agent-centered direction—that is, toward removing humans from the loop. Claude Code and Codex are already developing products in ways that remove much of the HITL, and the tools produced by those teams can be interpreted through the same lens.

Personally, simplifying software engineering around HITL and deliberately ignoring the other variables allowed me to treat everything else as noise—or, since this is a lens, to leave it blurred. That relieved a considerable amount of the motion sickness.

## 4. Using the HITL lens to predict what comes next

Another use of this lens is **prediction**. If we closely examine where HITL remains in the current process, we can make a reasonable guess at the tools and technologies likely to appear next.

If we call the long flow from business requirements through software engineering, deployment, operations, and incident recovery the business life cycle, today's agentic engineering mainly covers **only the software-engineering section in the middle**.

{% raw %}
```mermaid
flowchart LR
    R["Business<br/>requirements"] --> E["Software<br/>engineering"] --> D["Deployment"] --> O["Operations"] --> F["Incident<br/>recovery"]
    R -. HITL .-> R
    D -. HITL .-> D
    O -. HITL .-> O
    F -. HITL .-> F
    classDef done fill:#cfe8cf,stroke:#3a3;
    classDef todo fill:#f5f5f5,stroke:#bbb,stroke-dasharray:4 3;
    class E done;
    class R,D,O,F todo;
```
{% endraw %}

In the figure above, software engineering is colored green because HITL is being removed rapidly there. People are still involved in the remaining gray sections.

Through this lens, the next goal appears naturally. Once the mission of removing HITL from software engineering is largely complete, methodologies and tools will emerge to automate the human intervention that remains in the stages that follow: deployment, operations, and incident recovery.

A little later, I expect attempts to automate even **business-requirement analysis**, which today begins with a person and ends with a person.

## 4. What lens does our organization wear?

If we define a lens as the perspective an organization uses to interpret phenomena and the direction in which it tries to move, we can identify that lens by watching its behavior rather than listening to what it says.

In my personal classification, OpenAI and Anthropic are leading examples of companies wearing an agent-centered lens. Google appears somewhat neutral, while AWS and Cursor look like leading examples of companies wearing a human-centered lens.

This difference also appears in organizational structure. One clear signal is whether the company has roles such as the **AI Deployment Engineer, or AI DE**, and the **Forward Deployed Engineer, or FDE**, which I will discuss again below.

{% raw %}
```mermaid
flowchart TB
    L{{"Which lens<br/>does it wear?"}}
    L --> A["Agent-centered<br/>(OpenAI · Anthropic)"]
    L --> H["Human-centered<br/>(AWS · Cursor)"]
    A --> A1["Set HITL removal as the goal"]
    A1 --> A2["Harness engineering is essential"]
    A2 --> A3["Build AI DE · FDE teams<br/>Realign data · organizational structure"]
    H --> H1["Assume people remain<br/>Compromise at an appropriate level of automation"]
    H1 --> H2["The need for AI DE · FDE<br/>does not arise on its own"]
    H2 --> H3["Research · spread methods<br/>for human-centered AI use"]
    classDef agent fill:#dce8ff,stroke:#46c;
    classDef human fill:#ffe6d6,stroke:#e86;
    class A,A1,A2,A3 agent;
    class H,H1,H2,H3 human;
```
{% endraw %}

A company wearing an **agent-centered lens** asks how to automate the HITL that remains today.

If important information is exposed or arranged in ways that agents cannot easily access, making HITL removal difficult, the company will do everything it can to make that information accessible and usable by agents.

Harness engineering is essential for this work. When domain experts inside the organization have difficulty building the harness directly, the company will also create teams such as AI DE or FDE to support them.

Ultimately, the presence or absence of these teams offers an indirect view of the company's direction.[^2]

An organization wearing a **human-centered lens**, by contrast, always pursues an appropriate level of automation on the assumption that a person remains.

It hesitates to make complex adjustments or break down boundaries between individuals or between organizations. In the end, it compromises on the difficult parts of automation under the assumption that "a person will be there."

Because a person is always present at the important points under this lens, expectations for AI are not especially high. Harness engineering is needed only to an appropriate degree, so the need for roles such as AI DE or FDE does not arise on its own.

The visible signals also differ.

Human-centered companies either lack AI DE and FDE roles or, when they have them, the roles are closer to solving problems with agents than automating organizational work through agents. These roles are probably closer to quickly building PoCs and MVPs.

These companies do not talk much about harness engineering. Instead, they research and spread various methods in which people remain at the center while using AI.

Put differently, they build strategies and explain the world on the assumption that **AI will not improve beyond its current level, or will improve only linearly**.

Agent-centered companies, by contrast, show little interest in the human-centered side.

For them, the goal of AI DE and FDE roles is to automate the organization's work through harness engineering and help realign data and organizational structures around that goal.

> As an aside, I think FDE is currently the most self-destructive role. I can picture today's Solutions Architects, or SAs, shrinking substantially and being replaced by FDEs, only for the FDEs themselves to disappear a little later. This is pure speculation too, but there is a great deal more I could say about it.

Seen through this lens, the conclusion leans in one direction.

As token prices fall rapidly and the methods and tools of harness engineering improve, the gap between **token value and business value** will gradually narrow. When that happens, I think **the human-centered lens will ultimately be rejected, at least within agentic engineering**.[^6]

At some point, the rising curve of the side that began by removing people will overtake the ceiling of automation built around the compromise that a person will remain.

> Physical AI companies can actually be divided in roughly the same way.[^3]

## 5. Once you choose a lens, what will you do?

Finally, once you choose a lens, you need to decide **what to do with it** and begin moving.

If LLMs stop improving at their current level and ultimately fail to replace software engineering, what will I do?

> Agents may never reach the AGI that academia expected. But that possibility assumes we keep the current direction of building AI for self-improvement. If every company changed direction and concentrated its data on automating software engineering at today's level, I think capability that is effectively AGI-level is already possible within that narrow scope. This is another topic large enough for its own article, so I will leave it there.

Either way, we cannot avoid learning agent technology.

Codex and Claude Code already generate 90 to 100 percent of the code using only today's technology.

A person may still decide what ultimately gets accepted, but it is reasonable to say that the intermediate process has already been conquered. This does assume a nearly unlimited supply of tokens, but hardware advances will reduce token costs rapidly anyway.

Conversely, if it is already settled that agents will eventually replace software engineering, what should I prepare now?

Everyone will have ideas that come to mind and choices they have already made. Even this thought experiment alone can produce many entertaining scenarios.

Either way, **the purpose of a lens is not to make the lens itself. Its purpose is to decide your next action through it**.

So even if each person chooses a different direction for that action, I hope everyone has at least one lens of their own for looking at a phenomenon.

## Conclusion

Grinding a lens—bringing some parts into sharper focus while intentionally leaving others blurred—is more enjoyable than one might expect. Any phenomenon contains so many variables.

More than anything, finding one plausible lens that explains what is happening reduces stress. (Cue Ki-young's head over a one-minute candlestick chart.)

We are usually stressed when **prediction is impossible**—that is also what causes motion sickness—and a good lens gives us some freedom from that stress.

It leaves room to think about a world and a current we cannot control. That space also gives us the courage to take the next action.

That is what I ultimately wanted to say in this post. I am not trying to impose one correct lens, but to describe the value of the act of having a lens itself.

One downside of my current company is that everyone has different interests or serves different customers, so there is no one with whom I can have conversations like this. Even when I go out of my way to organize and explain my thoughts, many people disagree, so having the conversation only becomes tiring.

My goal is to change jobs around the end of the year. I hope either that my side projects go well enough for me to start a company on my own, or that I can work at a company with many people who see the world through a lens similar to mine.

I also started posting on LinkedIn because we live in an era when the messenger matters more than the message, and I wondered how I could increase my value as a messenger. It did not have much effect. (It is equally difficult for a capital-I introvert to survive online or offline.)

In an era when writing and code are cheap, a messenger's value seems to lie not in a few lines on a blog or LinkedIn, or a few lines of code on GitHub, but in the trail that person has created.

My trail so far has been unimpressive, but focusing on meaningful side projects and producing results from now on will be better than writing a few more lines like these.

---

[^1]: [Agentic Engineering and Transitional Technologies](/en/2026/05/11/direction-of-agentic-engineering.html).

[^2]: [The Next Evolution of Agents Will Come from Smarter Tools](/en/2026/05/27/agent-evolution-smart-edge.html).

[^3]: [Demystifying Harness Engineering](/en/2026/03/15/harness-engineering-beyond-context-engineering.html).

[^4]: [The Future Agentic App Engine](/en/2026/04/17/future-agentic-app-engine.html).

[^5]: Kent Beck, [The Product Development Triathlon](https://medium.com/@kentbeck_7670/the-product-development-triathlon-6464e2763c46) (2016). The original article introducing the 3X model of Explore, Expand, and Extract.

[^6]: [Why AI Adoption Should Not Start with Token Savings — The 3S Stages 1/2](/en/2026/06/15/organizational-ai-adoption-3s.html).
