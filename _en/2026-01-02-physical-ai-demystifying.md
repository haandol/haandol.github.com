---
layout: post
title: "Demystifying Physical AI"
excerpt: A practical introduction to Physical AI and robot learning
author: haandol
email: ldg55d@gmail.com
tags: physical ai nvidia isaac-sim
publish: true
lang: en
date: 2026-01-02 00:00:00 +0900
translation_key: physical-ai-demystifying
korean_url: /2026/01/02/physical-ai-demystifying.html
permalink: /en/2026/01/02/physical-ai-demystifying.html
---

## TL;DR

- Physical AI is a way to control motors with AI.
- The field divides broadly into foundation-model-based and IL + RL approaches, with diffusion becoming the dominant method for motor control.
- In the end, it is a competition over data.

## Introduction

In early 2024, I worked with a customer on a project that used an LLM to control a robot.

I knew nothing about robotics, the customer knew nothing about AI, and neither of us knew anything about VLA—Vision Language Action—so I spent a great deal of time on research at the beginning.

Even then, ChatGPT made papers much easier to read. I worked through RT-1, RT-2, RT-X, SayCan, L2R, VoxPoser, Eureka, Diffusion Policy, and anything else I could find. My eventual conclusion was that robotics data was vastly more important than it was for LLMs. The Covariant CEO whose work had been the starting point of my initial discussion with the customer had also previously worked at OpenAI before leaving to start an independent company in order to accumulate robotics data.

That led me to think we first needed an environment in which data could be collected easily. Given the customer's situation, a simulation environment seemed appropriate, and an LLM was an ideal way to generate robot code automatically for a variety of tasks.

Using papers based on similar ideas—the combination of robots, simulation, and LLMs—as references, I built a demo that manipulated a robot in simulation using only vision models and an LLM.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Wc842kGRkf4?si=3mSxB0Rla0Sg40qm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

I developed the system in the video further into a manipulation task that selected an arbitrary can from a three-level cabinet and brought it down. Simple as the task may sound, it could complete the desired work in simulation with a success rate of around 80 percent.

Through the customer's subsequent efforts, the same system was deployed to a real robot arm and demonstrated at re:Invent and internal events.

I then left the area completely alone, but growing interest in Physical AI recently led me to look into it again.

Even two years later, NVIDIA's—and perhaps Physical AI's—initial direction and methodology seemed to remain almost entirely unchanged. I also thought that organizing what I had studied briefly during that time might help me continue learning.

This post therefore summarizes what is useful to know when beginning Physical AI and offers a simple study order.

## Physical AI

Put simply, Physical AI is a way to control motors through AI.

There are broadly three ways to control motors with AI:

1. IL + RL approaches, such as Unitree G1 locomotion
2. Foundation-model-based approaches, such as GR00T N1
3. Approaches that combine the two appropriately, such as π₀ and RT-X

I think I first encountered the term Physical AI in Jim Fan's TED talk.[^1] Watching that video first and then the presentation below, given on the same subject two years later, makes the idea easier to understand.

<iframe width="560" height="315" src="https://www.youtube.com/embed/7fDiui8cAVQ?si=UWWxTNyBhNcjOY3x" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Personally, I think knowing the services in NVIDIA Omniverse will be highly advantageous when studying Physical AI in the future. The video provides a useful basic understanding of the roles NVIDIA's services play in the Physical AI development process.

## Essential Robotics Knowledge

When controlling robots in Physical AI, the most common representation uses the final joint, called the end effector, and describes it with seven degrees of freedom: `(x, y, z, roll, pitch, yaw, gripper)`.

It is therefore enough to understand the coordinate-system concepts that determine `(x, y, z)`, along with the axes that determine `(roll, pitch, yaw)` and the concept of axis rotation represented by quaternions.

Going slightly further, it is also useful to understand the basic concepts of forward kinematics and inverse kinematics, which explain how `(x, y, z)` maps to adjustments in the robot's joint angles.

As more Physical AI hardware manufacturers emerge, I expect robots to include features such as MPC—Model Predictive Control—and collision detection, allowing developers to focus more on business logic than robot control.

For an ordinary developer rather than a robotics developer, trying to learn the enormous body of robotics knowledge from the beginning leads nowhere. Understanding only the basic concepts above should be enough to read the code and operate a robot.

## Imitation Learning and Reinforcement Learning

The methods used to control robots in Physical AI have evolved in the order IL → IL + RL → foundation models. Each new approach emerged to overcome the limitations of the previous one.

### IL (Imitation Learning)

In imitation learning, an expert demonstrates a task and the model learns to follow that demonstration as closely as possible. Many people beginning Physical AI today train ACT—Action Chunking Transformer—with LeRobot. ACT is a representative model designed for imitation learning.

The advantage of imitation learning is that demonstration data alone can quickly produce something that at least works. Its limitations, however, are clear. An imitation-learning policy follows the demonstration distribution, so it cannot respond when the situation departs even slightly from the demonstrations—for example, when an object is in a different position, the lighting changes, or a grip fails.

### IL + RL

Reinforcement learning is combined with imitation learning to overcome those limitations. Reinforcement learning proceeds through endless trial and error to maximize the value of a reward function.

A common practical approach is to first make the behavior work with imitation learning—a warm start—and then improve its performance and robustness with reinforcement learning—a fine-tune. Imitation learning teaches the basic behavior and keeps the robot from making strange motions, while reinforcement learning adds the ability to recover from mistakes and remain robust across varied situations.

The IL + RL approach also has limits. Every task requires new demonstrations, a newly designed reward function, and new training. In other words, it does not generalize.

### Foundation Models (VLA)

Foundation-model-based approaches such as VLA—Vision Language Action—emerged to overcome this limitation. Just as an LLM handles many kinds of text tasks with one model, a VLA attempts to handle many robot tasks with one model.

The core idea is that a model pretrained on large-scale data can adapt to new tasks. Instead of training from scratch for every task, the user gives the desired task as a language instruction and the model performs it on its own.

In reality, foundation models alone do not solve everything, so many systems combine foundation models with IL + RL, as π₀ and RT-X do.

<iframe width="560" height="315" src="https://www.youtube.com/embed/ct4tdyyNDY4?si=fY5iJIOEiySN_of6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

The video shows the grueling journey through which Google DeepMind eventually arrived at the latest model, RT-X.

<iframe width="560" height="315" src="https://www.youtube.com/embed/AhyznRSDjw8?si=ykP8BPhZrYA6MVUT" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### Data Augmentation

The greatest challenge in Physical AI is the lack of data. LLMs can scrape text from the internet, but robot-control data cannot be obtained that way. Having people wear VR devices and control robots remotely through teleoperation produces high-quality data, but it cannot scale.

To solve this problem, methods for augmenting data with simulation and generative AI are advancing.

- Simulation 1.0 (digital twins): Simulators such as Isaac Sim generate data through large-scale parallel simulation and domain randomization. This approach still takes a long time.
- Simulation 2.0 (digital cousins): NVIDIA uses generative AI to augment data. Cosmos Transfer modifies environments, Cosmos Predict predicts future states, and GR00T Dreams uses a video world model as a neural simulator.

GR00T-Mimic in particular takes a small number of demonstrations—around ten—and automatically generates thousands of new trajectories. It expands the dataset by randomly changing object positions or modifying actions. Even if a person demonstrates a task only ten times, the robot can obtain an effect similar to practicing it thousands of times.

A video-based world model learns physical phenomena from billions of internet videos, which has the advantage of avoiding the need to program complex laws of physics one by one.

## Transformers and Diffusion

To understand Physical AI models at a high level, you need some understanding of transformers and diffusion.

### Transformers

Just as ideas across many vision models have moved from CNNs toward DiTs, transformer-based models are becoming dominant in Physical AI as well.

Consider the transformer we encounter most often: the LLM. It receives several tokens as input and outputs one next token.

<img src="https://substackcdn.com/image/fetch/w_800,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F495cca88-574b-4ace-b785-d6d6746e8f81_1500x504.png" />

The process is essentially the same when an image is the input. The only difference is that the image is divided into units called patches, converted into tokens, and then passed to the model.

<img src="https://substackcdn.com/image/fetch/w_800,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F266b718e-4118-4088-9ed7-1bb0f56b3478_1244x770.png" />

In other words, every transformer fundamentally works by receiving tokens and outputting the next token.

VLA—Vision Language Action—models are also transformer-based, so they receive tokens and output tokens.

The input converts `an image, text, and the robot's current state` into tokens, while the output converts motor-control commands into tokens. The basic form—token input followed by next-token output—does not change.

<img src="https://openvla.github.io/static/images/openvla_model.jpg" width="800" />

To explain the meaning more directly, the model can be understood as receiving the current frame's state and the goal to be achieved, then learning to output the action that should be taken in the next frame to reach that goal, much as a person would. OpenVLA is a representative model that works this way.

If actions are output one frame at a time, however, the model receives only the current state. It cannot know information such as the current movement speed, so the motion looks unnatural and tends to shake.

### Diffusion Models

Diffusion, which is widely used in image and video generation models, emerged to compensate for this problem. A diffusion approach injects noise into the input and trains the model to produce an output that predicts and removes that noise. In other words, it trains the model to predict noise.

<img src="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/consistency-models.png" width="800" />

One point to consider is that, as explained earlier, the original transformer input divides an image into patches. Diffusion predicts and removes noise, so it does not predict one patch at a time.

Generating an image by applying diffusion to a transformer—a DiT—means preparing enough tokens for the entire image in advance and predicting all token values together by removing noise, rather than generating the image one patch at a time in sequence.

Diffusion Policy, GR00T, π₀, and similar models apply this DiT approach so that they do not predict actions one frame at a time. Instead, from the current frame, they predict 50 actions—a trajectory—for how the robot should move over the next several dozen frames, for example the next 50.

Given the nature of transformers, some generated trajectories will naturally be wrong.

The robot therefore does not execute all 50 actions before generating the next trajectory. It executes only the first ten or so actions while immediately predicting the next trajectory.

It then corrects the motion by connecting the previously predicted trajectory with the new one appropriately, producing movement that is as natural as possible.

## ROS2

Traditionally, controlling a robot requires knowledge of ROS2. Unless you have a robot you need to control immediately, however, there is no need to study ROS2 yet. Running ROS on a MacBook is difficult as well.

It is better to become sufficiently familiar with robots in a simulation environment such as Isaac Sim first, then study ROS2 gradually when you actually need to control a physical robot.

## Study Order

It is easy to assume that studying Physical AI requires a robot arm and a GPU machine. In reality, it does not.

Setting a goal before you begin is a good way to avoid unnecessary cost. Unless a physical robot arm is essential to that goal, I recommend starting by controlling a robot in simulation.

### Cost

Let us first look at the approximate cost.

LeRobot is the common choice for a robot arm. I do not know how the claim that LeRobot costs $100 was calculated, but in practice it costs around 600,000 won.

It is certainly inexpensive compared with other robots and provides a well-developed environment for training and testing, but 600,000 won is not cheap enough for an individual to buy casually.

The GPU machine used for training and testing should be roughly equivalent to an RTX 4090. If you do not already own such a machine, buying one solely for this purpose is a considerable burden.

Controlling a dual-arm robot requires two LeRobot arms, a frame, and an additional depth camera such as a RealSense. At that point, collecting proper data usually requires a VR headset such as an Apple Vision Pro or Quest rather than controlling the system with two leader arms.

A dual-arm robot setup of this kind can cost as much as 10 million won in total. Personally, I think a single robot arm, or a robot arm plus mobility such as LeKiwi, is currently the upper limit for a hobby or personal interest. A few years from now, however, I think even humanoid robots may become hobby projects.

### Start with Simulation

In any case, if you want to explore Physical AI as a hobby as I did, I recommend beginning by controlling a robot in simulation rather than purchasing a physical robot.

I only have a MacBook, so I started by installing Isaac Lab and Isaac Sim on an EC2 g6.8xlarge instance and controlling the robot with a keyboard or a PlayStation or Xbox controller. This work needs much more CPU performance than GPU performance, so a 4xlarge instance can run it, but I used an 8xlarge.

Working through the Isaac Sim tutorials and then the Isaac Lab tutorials teaches most of what you need. The official LeRobot repository also provides USD files, making it easy to import the robot into the simulation.

After that, install GR00T on the instance, run a pretrained model once, then train and execute a simple manipulation task. At that point, you can consider yourself to have learned the basics of Physical AI.

<iframe width="560" height="315" src="https://www.youtube.com/embed/hsPQ-HluyPY?si=sEuW1UUPDSrFFTGb" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

I personally followed this process to fine-tune GR00T N1, ran Docker on my MacBook to study ROS2 with turtlesim, and did not buy a physical robot because I did not need one yet. I wanted to buy only a leader arm, but no one sold it separately.

### Set a Goal

From there, you can proceed according to your own goal: buy a LeRobot, study ROS2, augment and train data with GR00T Dreams, or buy only a Quest or Vision Pro and train a dual-arm or humanoid robot.

Physical AI means controlling a robot through AI, so unless you need to give a demonstration somewhere, I personally question whether buying a physical robot is necessary.

## Conclusion

The more I study, the more I think robotics ultimately comes down to a competition over data.

Robots that dance and perform various demonstrations have recently appeared in China, and most of them seem to use IL + RL approaches.

They demonstrate that a robot can perform a very small individual task well and offer to train it directly for the customer's desired work. I think this approach may ultimately be abandoned because of its limitations, but from the perspective of data collection, it does not seem like a bad direction.

As with Tesla's acquisition of autonomous-driving data, securing as much varied data as possible is important. Shipping products to users quickly and collecting field data therefore seems like a better strategy.

Ironically, Tesla is building robot farms to accumulate data, while China is acquiring data by shipping robots to users.

Meanwhile, NVIDIA and Google are trying to secure data by synthesizing it with generative models and even generating data that does not yet exist.

As the data competition between China and the United States begins in earnest, I find myself thinking more and more deeply about what to do as a vaguely defined jack-of-all-trades developer.

---

[^1]: [The Next Grand Challenge for AI](https://www.ted.com/talks/jim_fan_the_next_grand_challenge_for_ai)
