# Happy-Path Example — Thinking Engine

## Scenario

Developer asks: "We need to add real-time notifications to our app. Not sure how to approach it."

## Input Context

- App: Node.js backend, React frontend.
- Scale: ~5000 concurrent users.
- Infra: single EC2 instance, no message broker yet.
- Team: 2 engineers, 2-week sprint capacity.

## Expected Output

```text
problem:
- restatement: add real-time notifications to a Node.js + React app at ~5000 concurrent users within a 2-week sprint
- constraints: single EC2 instance, no message broker, 2 engineers, 2 weeks
- success-bar: users receive notifications within 2 seconds of the triggering event

assumptions:
- single instance means no horizontal scaling concern for this sprint — risk: medium if load spikes
- 5000 concurrent users is the peak, not average — risk: low; design for peak
- notifications are one-way (server → client), not bidirectional — risk: medium if requirements expand

options:
1. WebSockets (ws or socket.io): full-duplex persistent connection per client
   pros: low latency, well-understood, good React library support
   cons: stateful; harder to scale horizontally later; connection overhead at 5k users
   cost: medium

2. Server-Sent Events (SSE): one-way server-to-client stream over HTTP
   pros: simpler, HTTP-native, auto-reconnect, works with existing load balancers
   cons: one-way only; less ecosystem support than WebSockets
   cost: low

3. Polling: client fetches new notifications every N seconds
   pros: simplest to implement, stateless, horizontally scalable
   cons: latency = poll interval; wasted requests if no new notifications
   cost: low

recommendation:
- choice: Server-Sent Events (SSE)
- reason: one-way requirement fits perfectly; lower implementation cost than WebSockets;
  stateless design avoids future scaling pain; achievable in 2 weeks for 2 engineers
- blind-spots: if requirements expand to bidirectional (e.g., live chat), SSE becomes
  insufficient and migration to WebSockets will be needed

next:
- spike SSE implementation with EventSource on frontend (1 day)
- open: do notifications need persistence (i.e., shown to users who were offline)?
```

## Why This Is Correct

- Problem restated with constraints and success bar before options.
- Assumptions audited with risk if wrong.
- Three materially different options, each with pros/cons/cost.
- Recommendation includes a blind spot.
- Open question is concrete and blocks a design decision.
