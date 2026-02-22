# Context and Memory Management for AI Agents
**Architecture & Prototype Design Document**

## 1. Memory Types & Structure

### Categorization of Business Context
To effectively manage context, the system categorizes memories into four distinct layers:
1.  **Immediate Context (Working Memory):** High-frequency, transactional data relevant only to the *current* active interaction (e.g., the specific invoice details being processed, current cart items, current ticket error logs).
2.  **Historical Context (Episodic Memory):** Records of past interactions, transactions, and explicit events (e.g., past support tickets, previous POs, documented quality issues, payment history).
3.  **Temporal Context (Time-Series Memory):** Information that has a specific trajectory or validity period. This includes seasonal patterns (e.g., summer delivery degradation), SLAs, and expiring contract terms.
4.  **Experiential Context (Semantic/Knowledge Memory):** Synthesized lessons, generalized rules, and overarching relationship statuses (e.g., "Customer is a high-value enterprise client," "Supplier XYX requires extra QA").

### Data Structures for Storage and Retrieval
The system uses a **Hybrid Knowledge Graph + Vector Database + Time-Series Index** approach:
*   **Knowledge Graph (Entities & Relationships):** Nodes represent entities (Suppliers, Customers, Invoices, Issues). Edges represent relationships (`SUBMITTED_BY`, `EXPERIENCED_ISSUE`, `RELATES_TO`). This allows traversing related context (e.g., Invoice $\rightarrow$ Supplier $\rightarrow$ Past Issues).
*   **Vector Embeddings:** Interactions and textual context (e.g., customer frustration emails, unstructured logs) are embedded into high-dimensional vectors. This enables semantic Search (e.g., finding "similar integration issues").
*   **Metadata Annotations (Time-Series Data):** Every node and edge contains metadata schemas (Timestamps, Confidence/Importance scores, Decay rates) to support filtering and temporal decay logic.

### Linking Related Memories
Using the Knowledge Graph, memories are intrinsically linked.
*   **Example (Supplier Quality):**
    *   Node A (Invoice #123) $\rightarrow$ `BELONGS_TO` $\rightarrow$ Node B (Supplier XYZ).
    *   Node B (Supplier XYZ) $\rightarrow$ `HAS_HISTORY` $\rightarrow$ Node C (Quality Issue logged 4 months ago).
    *   When the Agent focuses on Node A, the graph traversal algorithm extracts subgraphs connected to Node B up to a degree of *N* (e.g., degree 2 uncovers Node C).

---

## 2. Context Hierarchy

### Prioritization Metrics
Context relevance is calculated using a **Proximity Score** ($P_{total}$) that combines three distinct metrics:
1.  **Temporal Proximity ($P_{temp}$):** How recent the information is. Recency usually implies relevance, modified by the memory's lifecycle rules.
2.  **Relational/Structural Proximity ($P_{rel}$):** How closely connected the information is in the Knowledge Graph (Graph Distance). Direct relationships (Degree 1) score higher than indirect ones (Degree 3).
3.  **Semantic Proximity ($P_{sem}$):** Cosine similarity between the current interaction's vector embedding and the historical memory's embedding.

**Final Score Calculation:**
$P_{total} = (w_1 * P_{temp}) + (w_2 * P_{rel}) + (w_3 * P_{sem}) * \text{Importance Factor}$
*(where $w_1, w_2, w_3$ are tunable weights depending on the task).*

### Handling Conflicting Information
When historical data contradicts recent data (e.g., Supplier was bad 6 months ago, but good for the last 3 months):
1.  **Staleness/Decay Overlay:** The older "bad" rating naturally decays over time (Temporal Proximity reduces its weight).
2.  **Trend Synthesis:** Rather than passing conflicting raw facts to the LLM, the Memory Manager synthesizes a trend summary node (e.g., "Supplier performance improved recently: 98% SLA in Q4 vs 70% in Q2"). The most recent *synthesized* experiential memory overrides older episodic memories.

---

## 3. Memory Lifecycle Management

### Staleness and Decay Rules
Information becomes "stale" based on a **half-life decay function** applied to its Temporal Proximity score:
$Score(t) = InitialScore * e^{-\lambda t}$
*   $\lambda$ determines the decay rate.

**Evergreen vs. Time-Sensitive Facts:**
*   **Time-Sensitive Facts** (e.g., a specific delayed delivery, a temporary bad mood of a client) have a high $\lambda$ (fast decay).
*   **Evergreen/Structural Knowledge** (e.g., "TechCorp is a Fortune 500 client", standard contract clauses) have $\lambda = 0$ (no decay).

### Archiving, Downweighting, or Deletion?
*   **Downweighting:** Stale information is first downweighted (relevance score drops below retrieval threshold). It is kept in the graph but skipped during fast-retrieval to save tokens/compute.
*   **Archiving:** If information drops below a lower threshold *and* hasn't been accessed in $X$ months, it is moved from "Warm Storage" to "Cold Storage" (database archive).
*   **Deletion:** Strictly reserved for data privacy compliance (GDPR/CCPA "Right to be Forgotten") or objectively obsolete system data (e.g., deprecated API versions). Business history is rarely deleted.

### Triggers for Memory Updates/Invalidation
*   **Explicit Invalidation:** A new contract is signed, triggering an event to invalidate (set decay to near-instant) the old contract parameters.
*   **Contradiction Threshold:** If $N$ consecutive positive interactions occur, the system triggers a background synthesis process to update the Experiential Memory from "Problematic" to "Improving/Reliable".

---

## 4. Retrieval Mechanisms

### Querying Efficiently & Preventing Overload
To scale to thousands of suppliers and millions of transactions without overwhelming the AI's context window:
1.  **Multi-Stage Retrieval:**
    *   *Stage 1 (Filter):* Hard filters based on direct Entity references (e.g., Only retrieve graph nodes directly linked to `Supplier_XYZ`).
    *   *Stage 2 (Rank):* Apply the Proximity Score ($P_{total}$) formula to all filtered nodes.
    *   *Stage 3 (Prune/Truncate):* Take the top $K$ nodes. If the context length exceeds the token budget, summarize the lower-ranked context before passing it to the LLM.
2.  **Lazy Loading:** The agent is given a high-level summary of the context first. If it needs deeper details (e.g., "CTO prefers technical deep-dives"), the agent can make specific sub-queries (Tool Use: `get_ticket_history(ticket_id)`).

### Addressing Key Questions
*   **Scaling:** The graph DB and Vector DB indices scale horizontally. The LLM only ever sees the pruned Top-$K$ results, keeping latency low.
*   **Emotional Context:** Yes, emotional context (frustration, urgency) is captured as metadata on Interaction nodes. It decays exceptionally fast (a frustrated customer 2 years ago shouldn't dictate today's tone if they've been happy since), but recurring frustration triggers a "High Churn Risk" experiential flag.
*   **Data Privacy:** Graph nodes have Role-Based Access Control (RBAC) tags. A Level-1 support agent's context retrieval will automatically filter out nodes tagged `RESTRICTED_FINANCE`.
*   **Explainability:** Because relevance is calculated mathematically via the Proximity Score components ($P_{temp}, P_{rel}, P_{sem}$), the system can trace *why* a memory was retrieved (e.g., "Retrieved because: Strong relational distance (Degree 1) and exact semantic match").
*   **Multi-Agent Shared Context:** The Knowledge Graph acts as a centralized "Hive Mind" repository. Agent A (Sales) updating a customer's node immediately changes the relational context for Agent B (Support), ensuring consistency across the enterprise.
