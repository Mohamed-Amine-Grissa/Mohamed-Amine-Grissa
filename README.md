<img src="./assets/hero.svg" width="100%" alt="Mohamed Amine Grissa. Computer science engineering student at ISSAT Sousse. Backend systems in Java, and evaluation of language models."/>

I am a computer science engineering student at ISSAT Sousse, Tunisia, and artificial intelligence is the part of this field that I want to be excellent at. Neural networks and large language models are what I study when nobody asks me to. I want to understand how they learn, why they fail, and how to prove that one is good enough before anyone depends on it. That is why my internship was about evaluation: I ran local models on a laptop CPU and measured them, because a model that only looks good is not good.

I am also a software engineer, and I think that matters for AI. A model is useful only when it runs inside a system that works, so I build that system too: services in Java and Spring, messaging with RabbitMQ, secured APIs. My goal is to become an AI engineer who can take a model from an experiment to something people can rely on.

The handle comes from Norse mythology. Ratatoskr is the squirrel that carries messages along the world tree. Most of what I build moves messages too: between services or into a model and back.

## Selected work

### [Foundation Models Evaluation](https://github.com/Mohamed-Amine-Grissa/Foundation-Models-Evaluation-Internship)

An internship project. Five weeks of experiments on local language models, on a laptop CPU, with `llama.cpp`.

<img src="./assets/pipeline.svg" width="100%" alt="Evaluation pipeline: prompt, local LLM, metrics, LLM judge, scorecard."/>

- I measured perplexity, lexical and semantic similarity, and the functional correctness of generated code (pass@k).
- I wrote a rubric for an LLM judge, labelled the answers myself, and measured how often the judge agreed with me.
- I ranked models with pairwise comparison and an Elo-style score.
- I combined quality, cost and latency in one scorecard, then used it to compare zero-shot, few-shot and chain-of-thought prompts.
- I tested the prompts against prompt injection.

`Python` `llama.cpp` `GGUF` `Qwen2.5` `Llama 3.2` `Phi-3.5` `LaTeX`

### [Spring Boot Microservices Labs](https://github.com/Mohamed-Amine-Grissa/spring-boot-microservices-labs)

One e-commerce domain, built in five steps. Each step adds one architectural concern and nothing else: REST calls between services, a database for each service, service discovery behind an API gateway, stateless JWT security, and asynchronous messaging. The repository contains 15 Spring Boot services.

`Java` `Spring Boot` `Spring Cloud` `Eureka` `Spring Security` `JWT` `JPA` `RabbitMQ`

### [Java Middleware: RMI and RabbitMQ](https://github.com/Mohamed-Amine-Grissa/java-middleware-rmi-rabbitmq)

Nine projects on how two programs communicate when they do not share a process. The first half uses Java RMI, including stateful and thread-safe servers. The second half uses RabbitMQ with the default, fanout, direct and topic exchanges.

`Java` `RMI` `RabbitMQ` `AMQP` `Maven`

### AETHER

A simulation of a space agency that runs in the browser. It is written in JavaScript without a framework. It has a 3D scene, a mission planner with docking, refuelling and crew rest rules, a finance ledger that always balances, undo and redo, and automated tests. The code is not public yet.

`JavaScript` `Three.js` `Chart.js` `CSS Grid`

## Activity

<img src="./assets/contributions.svg" width="100%" alt="Contribution calendar for the last year. A ship fires at the calendar and each active day lights up."/>

## Skills

| | |
|---|---|
| **Backend** | Java, Spring Boot, Spring Cloud, Spring Security, JPA, REST |
| **Messaging** | RabbitMQ, Java RMI |
| **AI engineering** | Python, llama.cpp, embeddings, LLM-as-a-judge, prompt engineering, evaluation pipelines |
| **Web** | JavaScript, HTML, CSS, Three.js, Chart.js |
| **Networks** | Routing and switching, VLANs, ACLs, zone-based policy firewalls, Cisco Packet Tracer |

## Certifications and courses

| | | |
|---|---|---|
| **Cisco** | CCNA 2: Switching, Routing, and Wireless Essentials | Completed |
| **Google** | Google Developer Program courses | In progress |
| **Google** | Google Skills courses | In progress |

## Reading

I read a chapter, then I build what the chapter describes.

- **AI Engineering**, Chip Huyen (O'Reilly). Chapters 3 to 5 became the [evaluation repository](https://github.com/Mohamed-Amine-Grissa/Foundation-Models-Evaluation-Internship).
- **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow**, Aurélien Géron (O'Reilly).

<!-- Contact: add your links, then remove the comment markers.
## Contact

[LinkedIn](https://www.linkedin.com/in/YOUR-HANDLE) · [Email](mailto:YOUR-PUBLIC-EMAIL)
-->
