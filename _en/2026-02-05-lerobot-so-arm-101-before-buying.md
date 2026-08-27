---
layout: post
title: "What to Know Before Buying a LeRobot SO-ARM101 (Physical AI)"
excerpt: The real cost and setup behind a LeRobot SO-ARM101
author: haandol
email: ldg55d@gmail.com
tags: physical-ai lerobot so-arm-101 robotics
publish: true
lang: en
date: 2026-02-05 00:00:00 +0900
translation_key: lerobot-so-arm-101-before-buying
korean_url: /2026/02/05/lerobot-so-arm-101-before-buying.html
permalink: /en/2026/02/05/lerobot-so-arm-101-before-buying.html
---

## TL;DR

- It costs at least 600,000 won, not $100.
- It requires much more time and space than expected.
- You need a local GPU machine.

## Introduction

Around the year before last, I tried my first Physical AI project and bought a robot arm from AliExpress. It cost 170,000 won in total and was controlled with an Arduino and a gamepad. I bought it without much thought because it seemed cheap, but after trying various things with it, I began to wonder, "If I am studying Physical AI as a hobby, do I really need a robot arm?" AI is controlling the physical system, and AI is the core, so is the physical part truly necessary? My home is small too.

That led me to think there was plenty I could do in simulation and that, once foundation models and world models advanced far enough, perhaps the sim-to-real gap would disappear anyway.

Then I saw Reachy Mini from Pollen Robotics. It is a robot with virtually no practical utility, but it was enormously popular. That made me think, `Ah, if I want people to notice, I still need to work with a physical robot after all`, so I bought a LeRobot arm.

This post is something like a postmortem: a record of what I wish I had known before buying the robot arm.

![Robot setup](/assets/img/2026/0205/setup.jpg)

## 1. Think Once More About Whether You Really Need One

After buying it and running through everything, my conclusion was that the value for money was poor. I felt that way even after accounting for the fact that testing the same things without LeRobot would have cost more.

Everything could be tried in simulation anyway, and because AI is ultimately the core of Physical AI, the robot itself was not strictly necessary. If I could have rented one for about a month, I think I would have been better off not buying it.

## 2. It Costs More Than You Expect

I wish people would stop claiming that it costs $100. The printing alone seems to cost about $100. Compared with the 6DoF arm I bought from AliExpress, whose motors were each wired to and controlled by an Arduino, the LeRobot motors are relatively smart motors. They are controlled by bus ID from a single master bus, which makes the overall configuration extremely simple. The tradeoff is that each motor costs about 30,000 won. With six motors in each of the leader and follower arms, 12 × 30,000 means the motors alone cost more than 360,000 won.

You also need two cameras—one on the wrist and one overhead—a USB hub, 12V and 5V adapters, clamps, buses, and other parts. Together, these push the total above roughly 450,000 won. If you order directly from overseas through a seller such as WowRobo, customs duties apply, bringing the cost to around 500,000 won. Customs duties are charged when the combined price of the goods and shipping exceeds $150. In any case, you should budget at least 600,000 won and think carefully about whether it is worth that much.

## 3. It Requires More Time and Space Than You Expect

Even apart from the money, it requires a fair amount of space. You need room to install both the leader and follower arms, room for the cameras, and a layout that lets you connect power cables to both arms. It takes up quite a bit of room. My wife and I already live rather tightly in a 15-pyeong home, so having to invest space was actually a bigger problem for me than the money.

It also takes a fair amount of time. If you have never assembled one before, assembly will take about three hours—it did for me—and collecting a dataset takes another hour or two. If you can afford it and do not particularly need the experience of assembling a robot, paying roughly another 100,000 won for a fully assembled product does not seem like a bad choice.

If you have not worked with vision-based machine learning before, collecting the dataset will also involve trial and error. The lighting may be uneven, for example, or the overhead camera may not cover the entire scene and objects may repeatedly become occluded in certain situations. If the dataset is collected poorly, GR00T may tolerate it reasonably well, but ACT is unlikely to work well, so you may have to collect the data again.

Both videos below show results from collecting data locally with the leader arm, training on EC2, and bringing the trained model back to the local machine for execution.

First is a real-world demonstration trained with ACT.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Kwr9zjF7PXA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Next is a demonstration with GR00T.

<iframe width="560" height="315" src="https://www.youtube.com/embed/6gJNV_hN0dM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 4. You Need a Local GPU Machine

I do not have a computer at home, only a single MacBook Pro provided by my company. From the beginning, I planned to train the models on AWS because employees can use it almost without limit for experiments.

Most environment setup documentation assumes an NVIDIA Linux machine. If you do not have one, you need to begin with the assumption that you will use a cloud GPU.

On an AWS G6e.16xlarge instance, the training itself seemed to take roughly three hours for ACT and six hours for GR00T N1.5. Training can be faster with multiple GPUs. I needed to run Isaac Sim and experiment with various things, so I chose a machine with a high vCPU count and ended up using g6e.16xlarge.

A MacBook Pro is enough for collecting data and similar work. Training requires a GPU, however, and running the robot with the trained model requires a GPU again.

ACT, GR00T, and π₀ all use relatively small models, so they can run at around 5–10 Hz on a 16-inch M3 MacBook Pro with 48GB of memory. They struggle, but they do run. If your local machine is something like a MacBook Air or Surface Book, however, you will also need AWS GPU resources when operating the robot, so the cost will be higher than you might expect. At that point, it might actually be better to spend a little more and buy a Jetson Orin Nano.

## 5. Buying Only the Leader Arm Is Also an Option

As the heading says, buying only the leader arm is worth considering. One reason collecting data in simulation is difficult is that the resulting motion is less smooth than data collected with a leader arm. A SpaceMouse or joystick does not solve this easily either, though both are much better than keyboard control. ACT in particular uses imitation learning, so if the robot trajectories in the training data are not smooth, the success rate is likely to be very low.

For this case, it is not a bad idea to put everything in the cloud, connect the leader arm to Isaac Sim in the cloud, control the simulated arm, and use that data directly for training and inference in one place. Before my robot arm arrived, I did the same thing with an Xbox controller, and it worked surprisingly well.

Projects such as [LeIsaac](https://github.com/LightwheelAI/leisaac), which controls Isaac Sim through LeRobot, are also written on the assumption that Isaac Sim runs locally. I do not have a local NVIDIA environment, so I ran ZMQ alongside Isaac Sim on EC2 and used that queue to send action data from my local leader arm in real time, moving the follower arm inside Isaac Sim. You can see the related changes [here](https://github.com/LightwheelAI/leisaac/compare/main...haandol:leisaac:main). I wrote the entire implementation with Kiro, and thanks to Claude Opus 4.5, I confirmed that it worked after only a short debugging session.

In any case, a leader arm still gives you the feeling that you bought a robot while costing less than half as much because no cameras are needed, taking up very little space, and producing high-quality data. For those reasons, I sometimes think buying only the leader arm may be the best compromise.

## 6. For a Humanoid, Buy a Quest or Vision Pro

These days, people collecting data for humanoids do not control two leader arms like something out of *The Matrix*. They use a Quest or Vision Pro for gesture recognition. Rather than spending 1.3 million won on something like an XLeRobot with two arms, simply buying a Quest 3 may be a reasonable option.

That is roughly what I concluded after running through the setup. I already had these thoughts before buying it, and nothing particularly changed afterward.

One thing did change. When I showed people the same technology and the same process in simulation, everyone reacted as if to say, `So what?` When I showed it with a real arm, the response became, `This might actually be interesting.` The reaction was the same when I first worked on a Physical AI project in the past.

## Conclusion

As world models such as Cosmos Predict continue to improve and pipelines such as GR00T-Mimic and Dreams become more sophisticated, I increasingly think that, ironically, studying Physical AI may no longer require a physical environment.
