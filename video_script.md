# 🎬 Explaining the Dashboard Metrics (1-Minute Script)
*(Aim: Natural, casual tone. ~140 words. Focuses on what the specific numbers/labels mean.)*

---

**[Visual Setup]** 
*Have the Streamlit dashboard open (`http://localhost:8501`).*
*Ensure the sidebar is set to "Invoice QA (Supplier XYZ)".*
*Start Screen Recording your browser window.*

---

**[0:00 - 0:25] The Trigger & Context Breakdown**
"Hey everyone! Let's take a quick look at this UI I built for the AI agent memory system. On the left side, we have our 'Trigger Event'—a new invoice just came in. Now, look at the Context Cards on the right. These aren't just random search results; the engine actually scores them."

**[0:25 - 0:45] Explaining the Values**
*(Point to the top right card labeled 'Score: 2.333')*
"See this score up top at 2.3? That’s the 'Proximity Score'. It's a calculation based on how related the topic is, combined with the time distance. 

Down here *(point to the 'Age: 120d' label on the red Issue card)*, you see this red issue is exactly 120 days old. Normally, old data gets ignored by AIs, but the math correctly ranked this highly because the *severity* outweighed the age. 

And notice these ones that say 'Evergreen Policy' *(point to the green flag)*? Those are permanent rules, like this summer-delivery warning, so the engine completely bypasses the decay algorithm for them."

**[0:45 - 1:00] Conclusion**
"So basically, by calculating these precise timeline and relationship scores, the AI instantly knows exactly which historical facts are still relevant today before making a decision."
