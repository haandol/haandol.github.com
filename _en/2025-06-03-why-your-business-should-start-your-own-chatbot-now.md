---
layout: post
title: "Why Your Business Should Build Its Own Chatbot Now"
excerpt: Why your business should start its own GenAI chatbot now
author: haandol
email: ldg55d@gmail.com
tags: ai agent chatbot genai flywheel
publish: true
lang: en
date: 2025-06-03 00:00:00 +0900
translation_key: why-your-business-should-start-your-own-chatbot-now
korean_url: /2025/06/03/why-your-business-should-start-your-own-chatbot-now.html
permalink: /en/2025/06/03/why-your-business-should-start-your-own-chatbot-now.html
---

## TL;DR

- GenAI without a feedback loop is only half complete.
- Businesses with feedback loops accelerate the accumulation of high-quality data.
- Design the feedback loop first, then launch quickly.

## Introduction

My manager recently shared an insight about GenAI chatbots that strongly resonated with me. As I tried applying it to my current personal project,[^1] I came to agree with the perspective even more deeply.

I shared the insight on LinkedIn,[^2] but the format made it difficult to go into detail, so I will expand on it a little more here.

## The GenAI Flywheel

![GenAI flywheel](/assets/img/2025/0603/flywheel.png)

I drew the image above as a flywheel based on the insight I mentioned.

I think this perspective applies across GenAI as a whole, so it does not necessarily have to take the form of a chatbot. I will nevertheless explain it through chatbot UX because that form is the easiest to relate to, thanks to ChatGPT.

As I wrote in my post about building a flywheel,[^3] a flywheel always starts with the `goal` on the right, and improving the customer experience is a goal that never fails.

Let us consider an example in which we add a chatbot to Naver Shopping.

Previously, customers could search for products only within the limited framework of keywords and categories.

We improve that experience by launching an agent chatbot on Naver Shopping with basic search functionality provided as a tool. (Customer Experience)

Customers who are already familiar with GenAI through ChatGPT begin writing queries in more varied forms, such as `a swimsuit that hides my upper arms well in summer`. (Detailed Preference)

The original keyword- and category-based search API will probably still be running behind the scenes.

But because the search terms are transformed into the customer's core concepts—`summer`, `upper-arm fat`, `upper-body coverage`, and `swimsuit`—we can expect more appropriate results than the customer would have received by entering keywords directly.

If the customer clicks a product through the chatbot and goes on to purchase it, we learn new information about both the customer and the product we sell.

- On the customer side, we can learn that `because the customer is reluctant to expose their upper arms, it would be helpful to recommend clothes that cover much of the upper body, even when they are not swimsuits`.
- On the product side, whether or not the detail page says so, we can learn that `this product is good at covering the upper body, especially the arms`.

This is hidden information that was not previously available: latent information.

If we regularly incorporate this information into customer profiles and product data, then use it to generate parameters when calling the search API, we can improve the quality of search results even further. (Personalized Search)

The moment customers recognize that their preferences are reflected in the search results, they begin entering more detailed information. (Customer Experience leads to Detailed Preference)

Once this virtuous cycle has been created, it keeps turning, helping us understand customer preferences better and provide more accurate search results. (Personalized Search leads to Customer Experience)

That is what the flywheel above is meant to show.

### The Feedback Loop Matters Most

The most important thing to consider is a feedback loop in which the chatbot improves itself from users' experiences as they use it more.

A chatbot without this loop is merely another feature. Such a chatbot does little to improve the user experience that was its original goal.

![Naver Shopping search screen](/assets/img/2025/0603/naver-shopping.png)

Consider Naver Shopping, one of the best-known shopping sites in Korea. The example would be no different with Coupang.

Almost no one enters the kind of detailed query described above into Naver Shopping's search box. Even Naver does not want them to.

Customers have learned from experience that natural-language search queries will not be processed, and Naver cannot actually process them.

Simply attaching a chatbot does not solve this problem dramatically. When natural-language search is first introduced, users will try a wide variety of queries. Eventually, however, they learn through experience what works and what does not.

**Over the long term, the level of detail we can obtain from customers through the chatbot therefore converges on the level the chatbot can process.**

If the chatbot's performance does not improve along with the volume of customer input, it becomes an ordinary feature whose ROI converges toward a loss.

#### Example: ChatGPT's Image-Generation Feature

![ChatGPT image-generation example](/assets/img/2025/0603/chatgpt-image-generation-1.png)

ChatGPT could generate images even before the explosion of Ghibli-style images.

Very few people, however, thought about making something with images generated by ChatGPT.

After a feature update a few months ago, people learned that it could generate images at a quality level that looked as if Studio Ghibli had drawn them. They then began uploading large volumes of **personal photos—which were also training data** that they ordinarily would not have uploaded to a service.

Before image-generation quality improved, people uploaded almost no personal photos. Once the quality reached a certain level, users voluntarily began contributing large volumes of personal images.

Through many different attempts, they quickly discovered the feature's limits and eventually generated images in ways that matched where its capabilities converged.

![Another ChatGPT image-generation example](/assets/img/2025/0603/chatgpt-image-generation-2.jpg)

Known limitations remain, including consistency problems and difficulty understanding detailed objects from text. Even so, users now provide many kinds of inputs in ways they would not previously have tried because those results were believed to be impossible.

The point is that if a chatbot merely appears to understand detailed requirements, users will willingly share detailed preferences. Over time, the level of detail that users voluntarily share will match the level the system can actually process.

### Start by Adding a Chatbot

Launching the chatbot is more important than making the feedback loop perfect. I mean that it should launch even if the loop is incomplete, not that it should launch without any loop at all.

Traditional analytics methods provide only indirect estimates of user behavior. Log analysis, click tracking, and purchase records can all tell us **what** a user did, but it is difficult to know **why** they did it.

A chatbot, by contrast, lets us ask questions in the user's own language and receive direct answers. It can provide insight into why users search, what they value, and how they make decisions. These insights are difficult to extract through conventional methods.

The moment a simple loop lets you learn one more thing about customers and reflect it in the product, you move that one step ahead of other services. The ChatGPT example above demonstrates why moving first in that market matters.

Google's Imagen has much stronger image-generation capabilities, but Google will find it difficult to obtain as much personal-image data as ChatGPT has. The difference was probably influenced by both first-mover advantage and the competitive advantage ChatGPT already had as a GenAI service.

This is where the difference between being recognized as a GenAI service through a single loop and failing to establish that identity comes from.

### Put the Chatbot Where You Want to Improve the User Experience

I sometimes see chatbots placed everywhere indiscriminately, followed by the claim that the product is now a chatbot service.

You might think this is better than having no chatbot at all. But users do not provide meaningful data to such chatbots, and I question whether the service is collecting that data in the first place, let alone trying to do anything with it.

So where should a chatbot be placed?

To answer that question, you first need to decide what more you want to learn from customers. That question is connected to the feedback loop.

In other words, you need to decide which part of the customer experience you want to improve before you can determine both the feedback loop and the chatbot's location.

### Launch Quickly and Design the Data Pipeline First

GenAI makes it possible to reach 90 percent usability very quickly.

But because it is GenAI, the remaining 10 percent cannot be completed without the right context and data pipeline.

That missing 10 percent can ultimately be filled only through operational experience and real user data, a point that is easily overlooked, especially in enterprises.

Many businesses hesitate until they can launch at 95 or 100 percent, but for chatbots, I think launch speed matters.

The sooner a chatbot launches, the sooner it can create a feedback loop, and that feedback loop can improve the chatbot more quickly.

A chatbot with a data pipeline that collects inputs, cleans them, and feeds them back into the system becomes stronger over time through user data. Users naturally provide more information to a system that is intelligent and responsive.

What matters here is that a chatbot is not merely an interface. It is both a tool for gathering rich user insights and an engine for continuous product evolution.

In the end, clearly defining the user data you want, building a structure that converts that data into product intelligence, and, most importantly, launching the chatbot as quickly as possible become the same act as improving the product.

## Conclusion

As GenAI in its current form spreads through every domain, context becomes increasingly important.

In business, context is the data a company accumulates, and how differentiated that data is from the data of other businesses will become increasingly important.

We may be entering a world in which data differentiation alone becomes the reason a business exists. In that competition, I expect the winner will be the side that starts accumulating **meaningful data** even one day earlier.

Perhaps the chatbot will become the unified interface for every product.

It may eventually become voice or motion instead, but only the input modality will change. Everything behind it will remain the same as today's chatbot.

The chatbot you deploy today can therefore become the competitive advantage that defines your business tomorrow.

---

[^1]: [EncBird](https://www.encbird.com)
[^2]: [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7321069291301150722/)
[^3]: [How to Build a Flywheel for a Startup](/2022/10/22/thoughts-on-flywheel-for-startup.html)
