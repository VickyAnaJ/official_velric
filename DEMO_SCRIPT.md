# Unified Demo Script

“This project is Ops Graph, a walker-native incident response system built for mission-critical inference infrastructure.

The reason this matters is that in military simulation and training environments, infrastructure failures are not just technical problems. If an inference stack degrades, it can interrupt scenario generation, reduce training continuity, delay evaluation cycles, and weaken operator trust in the system. So the challenge is not just detecting incidents. The challenge is responding quickly, safely, and in a way operators can understand.

That is why we used Jaseci.

Jaseci is a strong fit because this is fundamentally a graph problem. Incidents are connected to alerts, metrics, deployments, routes, configs, policies, and actions. In a traditional architecture, that context is fragmented across monitoring tools, backend services, dashboards, and human runbooks. Operators have to mentally reconstruct the relationships before they can decide what to do. That increases cognitive load and slows recovery.

With Jaseci, those relationships are first-class. The graph becomes the operational model, and walkers become the orchestration mechanism for how the system moves through that model. Instead of stitching together disconnected services, we can traverse the actual operational context directly.

We also chose this specific methodology very deliberately.

We did not want one unconstrained agent making opaque decisions in a high-stakes environment. We also did not want to rely only on traditional static rules, because rules alone become brittle when the context is dynamic and relational.

So we used a bounded staged workflow:

triage, plan, execute, verify, rollback, and audit.

That matters because each stage has a clear responsibility.

Triage identifies what kind of incident we are dealing with.
Plan generates a typed remediation path.
Execute applies only allowlisted actions.
Verify checks whether recovery actually happened.
Rollback restores a safe state if recovery fails.
Audit records the full sequence in operator-readable form.

This structure gives us bounded autonomy.

The LLM is used where it adds the most value, in interpretation, hypothesis generation, planning, and summarization, but it does not get unlimited authority. Policy gates, typed actions, verification logic, and rollback safeguards constrain the system.

That is the core reason traditional methods fall short for this workflow.

Traditional monitoring and runbooks are too fragmented and too manual.
A pure rules engine is too rigid.
An unconstrained LLM agent is too risky.

What this system does instead is combine graph-native context, staged orchestration, and bounded LLM reasoning. That gives us adaptive decision support without losing safety, explainability, or operator control.

For this demo, the frontend is intentionally deterministic. We hardcoded the demo states so the presentation is reliable and repeatable. That lets us clearly show the intended operational behavior without depending on live backend timing during judging.

Now I’ll walk through the three scenarios.

First, New Incident.

This is the standard autonomous recovery path. The system detects a high-severity canary issue, classifies it as capacity saturation, generates a remediation plan, passes policy evaluation, executes safe actions, verifies recovery, and records the result in the audit trail.

The key takeaway here is lower MTTR with traceability. The operator can see the incident, the hypothesis, the planned actions, the policy outcome, the verification result, and the audit log in one view.

Second, Rollback Demo.

This shows the safety path. The system identifies the issue and executes the remediation, but verification fails. Instead of assuming success, it triggers rollback and restores a known-good state.

That is important in military simulation infrastructure because failed automation cannot be allowed to deepen disruption. Recovery has to be validated, and if validation fails, the system must revert safely.

Third, Policy Block.

This shows the governance path. The system detects the issue and forms a plan, but confidence is below the policy threshold, so execution is blocked.

That demonstrates an important principle: good autonomy is not just about acting. It is also about refusing to act when confidence is insufficient. In high-stakes environments, restraint is a feature.

So the value of this project is not just faster incident response.

It is trustworthy incident response.

We use Jaseci because this is a graph reasoning problem.
We use walkers because incident response should be explicit and staged.
We use LLMs in a bounded way because decision support is valuable, but unconstrained autonomy is not acceptable in this domain.

The end result is a system that helps operators move faster while preserving policy control, verification, rollback safety, and full auditability.

That is why this methodology fits military simulation and training systems: it improves resilience without sacrificing trust.”
