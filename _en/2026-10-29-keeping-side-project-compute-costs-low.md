---
layout: post
title: "Zero Server Costs for Side Projects with AWS Native Serverless Architecture"
excerpt: Eliminating idle server costs for side projects on AWS
author: haandol
email: ldg55d@gmail.com
tags: aws serverless lambda s3-vectors agentcore side-project pmf cost-optimization
publish: true
published: true
date: 2026-10-29 00:34:56 +0900
last_modified_at: 2026-10-29 10:39:17 +0900
lang: en
translation_key: keeping-side-project-compute-costs-low
korean_url: /2026/10/29/keeping-side-project-compute-costs-low.html
permalink: /en/2026/10/29/keeping-side-project-compute-costs-low.html
---

## TL;DR

- Keep fixed operating costs low until product-market fit.
- Avoid continuously running application servers.
- Keep development and deployment affordable.

## Introduction

When building a side project or a business on my own, I would like users to arrive as soon as I launch. That rarely happens so neatly. The service still needs to run while I learn which problems matter and which features people keep using.

**I think it matters to be able to keep going until product-market fit (PMF), when the product meets market demand.** Learning from users and revising features takes time. Fixed costs accumulating across services make it harder to afford that time.

I build and operate [Encbird](https://www.encbird.com), an English learning service, and [PixelbankStudio](https://www.pixelbankstudio.com), an AI image editing service.

**The services are in different domains but share the same serverless architecture. When users are not using them, there is no compute charge for keeping application servers running.** Executing jobs, calling AI models, storing files, and transferring data have their own costs.

In this post, I want to share how to build and run a service cost-effectively when starting a solo business or side project.

## 1. Lowering the cost of keeping a service available

Hosting several services on one server can spread its cost across them. But I still pay for the time that server is running, even when nobody visits.

Encbird and PixelbankStudio serve their web interfaces as static files and run their backends on AWS Lambda. Lambda executes code in response to requests or events. Keeping a service available this way does not require a continuously running application server for each product.

The application interface is a Vue 3 single-page application (SPA). I chose client-side rendering (CSR), where JavaScript constructs the interface in the browser, to reduce the cost of server-side rendering (SSR), which generates HTML on the server for incoming requests.

The HTML and JavaScript files are stored in Amazon S3 and delivered through Amazon CloudFront. S3 stores files; CloudFront is a content delivery network (CDN) that caches and delivers them close to users.

CSR makes search engine optimization (SEO) more challenging because a search engine needs to execute JavaScript to read the page content. I address that by prerendering public pages that can be prepared in advance, generating their HTML at build time.[^1]

Encbird's landing and pricing pages are examples. They are deployed as HTML files containing the page content, so the server does not need to render them again for each incoming request.

Both services store data in Amazon DynamoDB using its on-demand capacity mode, which charges for reads and writes as they are used. I do not keep a separate database server running for either application.[^2]

That difference matters when requests are infrequent. Compute costs follow incoming requests and executed jobs more closely than the length of time the service has been available.

| Responsibility | Components | What contributes to cost |
| --- | --- | --- |
| Delivering web files and assets | S3 + CloudFront | Storage, requests, and data transfer |
| Handling API requests | API Gateway + Lambda | API requests and function execution |
| Storing and retrieving data | DynamoDB on-demand | Reads, writes, and storage |
| Processing background jobs | SQS + Lambda | Queue usage and job execution |

API Gateway connects incoming requests to the backend. Simple Queue Service (SQS) holds jobs for processing. Separating these responsibilities does not mean adding a continuously running server for each one.

### Moving to Go to reduce cold starts and memory use

Low compute costs between requests come with a possible delay when a new execution environment needs to be prepared. That delay is a cold start. The INIT phase, which starts the runtime and loads libraries and initialization code, is also billed. Since August 1, 2025, INIT billing has also applied to the previously exempt combination of managed runtimes, ZIP packages, and on-demand execution.[^3]

That is why **I think Go or Rust is worth considering when Python or TypeScript is not a requirement.** Running a compiled binary and keeping startup dependencies small can help reduce both memory use and cold starts.

Encbird's server was written in Go from the beginning. PixelbankStudio started in Python because part of the work involved loading and testing local models.

On a Lambda configured with little memory, I found that **the Python implementation's cold start took more than one second longer than Go's.** That difference led me to move PixelbankStudio's backend APIs and workers entirely to Go.

Language alone does not determine cost. Libraries, initialization code, and memory settings matter too. In my case, making the execution setup lighter with Go helped me run the backend on smaller Lambdas.

## 2. The AWS stack in use

**Encbird and PixelbankStudio share the same foundational architecture.** S3 and CloudFront serve the static web app, Lambda runs APIs and background jobs, and DynamoDB and S3 store the data.

The diagram adds scheduling, email, observability, and deployment support to that shared foundation. S3 Vectors for similarity search and Step Functions for multi-step jobs appear as options for workloads that need them. Multiple functions or stores with the same role are grouped together.

![The shared AWS architecture for Encbird and PixelbankStudio: web hosting, authentication, APIs, data stores, queues and workers, scheduling, email, observability, deployment support, and optional S3 Vectors and Step Functions.](/assets/img/2026/1028/shared-aws-architecture-en.svg)

### Encbird: separating learning requests from follow-up work

In Encbird, learners collect English expressions, practice them in conversations, and review them later. I described the learning design in an earlier post: expressions collected from conversations go into a shared dictionary that other practice features can use.[^4]

API Lambda functions accept learning requests, while follow-up work after a session ends travels through events and queues to separate Lambda functions. Moving lengthy processing, including model calls, out of the request means the API does not have to hold its response until the entire job finishes.

Amazon Cognito handles sign-in, DynamoDB stores learning data, and S3 stores images and other files. Where AI is needed, the backend calls model APIs. I do not operate GPU servers to host those models.

Simple Notification Service (SNS) distributes events. For example, a session-ended event is delivered to a queue, and a worker processes the queued work. A worker is a program that performs these background tasks; here, it also runs on Lambda.

EventBridge rules and Scheduler start work at specified times, and SES sends application emails. CloudFront Functions normalize file requests, while Lambda@Edge resizes images when needed. Caching the transformed result avoids recomputing it every time the same file is displayed.

CloudWatch provides logs, metrics, and alarms, with X-Ray for execution tracing. IAM manages execution permissions, and SSM Parameter Store holds configuration. ACM provides HTTPS certificates, and CloudFormation deploys the infrastructure defined in CDK. I do not operate separate servers for these supporting capabilities either.

Adding learning features can mean adding APIs and workers. Having more functions does not, by itself, create a bill for keeping a separate server running all day for each one.

Scheduled jobs and follow-up work can still incur costs when no user is online. What I have reduced is the compute kept running just to maintain availability.

### PixelbankStudio: editing in the browser, generating through jobs

PixelbankStudio lets users arrange and edit images on a canvas, then generate images with AI. Its web app is served statically, while Lambda runs the APIs for image uploads and generation jobs.

Moving and resizing images on the canvas happens in the browser. The server does not need to keep computing the canvas while a user edits it.

For uploads, I also avoided having an API Lambda receive an entire image and forward it to S3. The server issues a presigned URL, which grants temporary permission to upload a particular file, and the browser uploads directly to S3. Before subsequent processing, the server checks matters such as the file's ownership and intended use.

This keeps large image payloads out of API Gateway and Lambda. Lambda issues upload permissions and validates requests; S3 handles the file transfer.

Work such as image generation can take 30 seconds or more to produce a response, making it difficult to wait for completion within an ordinary HTTP API request. The API Gateway HTTP API used for this path has a maximum integration timeout of 30 seconds.[^5] The API therefore queues a job in SQS and returns its ID first. A Lambda worker then calls the model API and stores the result in S3. The browser checks the job's status and retrieves the completed file through CloudFront.

Some multi-step jobs, such as space generation and video import, use Step Functions to run their Lambda stages in sequence. EventBridge starts scheduled recovery work. Authentication, email, observability, permissions, and deployment use the managed services shown in the diagram; ECR stores images for Lambdas deployed as containers.

Calling models through external APIs removes the need to maintain my own GPU servers. Each generation incurs the model provider's usage charge instead.

Asynchronous processing separates long jobs from the request's time limit. Time spent waiting for a model API response inside a Lambda worker is still billed as Lambda execution.[^6]

Files have lifetimes too. Unused uploads and generation inputs have expiration policies, and incomplete multipart uploads are cleaned up. Separating results that users want to keep from intermediate files helps prevent storage costs from steadily accumulating after compute has been reduced.

### Splitting long jobs into stages and keeping compute on Lambda

Making the API asynchronous does not remove the maximum 15-minute limit on a single ordinary Lambda execution.[^7] An agent's overall task—researching information, calling tools, and revising its result—can take longer than that.

I therefore split long jobs into processing stages. Each stage finishes within its Lambda execution limit, with progress and results stored between stages. Step Functions connects the stages. The overall job can exceed 15 minutes without any single Lambda running for more than 15 minutes.

Amazon Bedrock AgentCore Runtime is another good option when one agent execution needs to stay alive for longer. Its serverless microVM configuration uses small virtual machines and can maintain an execution environment for up to eight hours.[^8] Consumption-based pricing follows actual CPU and memory usage, with no CPU charge for waiting on model responses when no CPU is consumed.[^9]

**For now, I find it easier to manage staged Lambdas and keep compute on Lambda.** That lets me continue using the deployment, permissions, and logging setup I already have. Moving to AgentCore Runtime is an option, rather than a requirement; my choice depends on whether I can split the work and how simple I can keep the execution environments I operate.

### S3 Vectors as an option for similarity search

Long-term memory and document retrieval sometimes need to find similar meanings expressed in different words. Similarity search represents text or documents as numerical arrays called vectors, then finds nearby vectors. Starting with a continuously running vector database can create maintenance costs even when searches are rare.

For Encbird's earlier long-term memory implementation, I replaced the Qdrant vector database with **Amazon S3 Vectors** for similarity search. S3 Vectors provides dedicated vector buckets and indexes, so I could store and query vectors without provisioning a separate vector database's compute capacity.[^10]

In the current Encbird code, the memory design has changed: DynamoDB holds records and references, while ordinary S3 snapshots hold memory content. This memory path does not call S3 Vectors. **Choosing S3 Vectors where similarity search is needed, and omitting that component where it is not,** is another way to keep costs low.

With S3 Vectors, I need to account for storage, writes, queries, and generating embeddings—the process of converting source content into vectors. Query charges depend on requests and the data processed, which reflects vector count and size in the index. Growing data or query volume calls for another comparison.[^11] Its value here is avoiding a continuously running vector server at the beginning.

## 3. Keeping development and deployment affordable

### Keeping dev and prod separate

I cannot try every feature change directly in production. A separate development (dev) environment lets me check changes with test data before applying them to production (prod).

Serverless pricing is useful here too. A development environment often receives requests only during testing. With Lambda and DynamoDB on-demand, having that environment ready does not require keeping application and database servers running continuously.

I define infrastructure with AWS CDK, a tool for creating and connecting resources such as Lambda functions, tables, and queues in code. Starting from the same infrastructure definitions, environment-specific settings can separate API addresses, tables, buckets, queues, and authentication configuration for dev and prod.

Changing an environment's name while pointing it at the same tables and queues would not separate it. The connections must also keep development requests and test data within the development environment.

**I can keep a development environment with a similar architecture to production while keeping its idle compute costs low.** There is less need to start and stop servers every time I develop just to save money.

Stored files, logs, and scheduled work still have costs. Lambda's Provisioned Concurrency also charges for keeping capacity initialized.[^6] The benefit described here assumes an on-demand setup without that continuously prepared capacity.

### Using GitHub Actions' included minutes for deployment

I also use GitHub Actions' included execution minutes for deployment instead of maintaining a separate build server. The web pipeline verifies the code, builds static files, uploads them to S3, and invalidates the CloudFront cache.

**GitHub Free includes 2,000 minutes per month for private repositories using standard Linux runners.** A runner is the environment that executes builds and tests. The allowance is shared across repositories owned by the same account or organization; it is not a separate allowance for each repository.[^12]

The workflows use Ubuntu runners. They run checks for the affected scope and reuse dependency and build caches to avoid unnecessary execution. PixelbankStudio's web deployment reuses the artifact produced during verification, so publishing does not require another build.

Keeping builds and deployments within the included minutes avoids adding a continuously running server on the development side as well. Artifact storage and the AWS resources receiving the deployment have separate costs to manage.

## Closing

I think this architecture fits side projects and solo businesses that are still looking for PMF. It keeps compute costs low while users are few and avoids adding continuously running servers for development and deployment.

The same principle can apply when trying another service: build around the work that actually runs and the data that must remain, rather than starting with another continuously running server. While learning which services people need, I want an environment where maintenance costs do not force an early end to an attempt.

---

[^1]: [Nuxt rendering modes](https://github.com/nuxt/nuxt/blob/main/docs/3.guide/1.concepts/1.rendering.md) — CSR and static deployment with build-time prerendering.
[^2]: [Amazon DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/) — on-demand reads, writes, and storage.
[^3]: [AWS Lambda INIT billing standardization](https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/) — effective August 1, 2025. Custom runtimes and container images were already billed for INIT before this change.
[^4]: [Connecting Encbird's conversation data to review features](/en/2026/03/12/genai-flywheel-for-business.html)
[^5]: [API Gateway HTTP API quotas](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quotas.html) — maximum integration timeout of 30 seconds. The article refers to this ordinary HTTP API path; separate REST API and response-streaming configurations have different limits.
[^6]: [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/) — requests, execution duration, memory, and Provisioned Concurrency. Diagrams use [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/).
[^7]: [Lambda execution timeout](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html) — ordinary Lambda configurations have a maximum execution time of 900 seconds.
[^8]: [AgentCore Runtime lifecycle settings](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-lifecycle-settings.html) — microVM execution lifetime and idle timeout. See also [async task tracking](https://github.com/aws/bedrock-agentcore-sdk-python/blob/main/tests_integ/async/README.md).
[^9]: [Amazon Bedrock AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/) — CPU and memory billing for consumption-based microVMs.
[^10]: [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) — vector storage and search without separately provisioned infrastructure.
[^11]: [Amazon S3 pricing](https://aws.amazon.com/s3/pricing/) — S3 Vectors storage, write, and query charges.
[^12]: [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) — GitHub Free for individuals and organizations includes 2,000 monthly minutes for private repositories. Standard GitHub-hosted runners are free for public repositories; artifact storage is accounted for separately from execution time.
