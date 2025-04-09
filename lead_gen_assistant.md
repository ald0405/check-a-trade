## 🎯 Lead Gen Voice Assistant Architecture

```mermaid
graph TD
    User("📱👷‍♂️ Tradesperson<br>🎤 Voice Input")
    MainAgent["🤖 Voice Assistant<br>'The Lead Gen'"]

    subgraph Check-a-Trade Swarm
        Metrics["📈 get_profile_metrics"]
        Ratings["⭐ rating_analytics"]
        ResponseTime["⏱️ response_time_checker"]
        Rewrite["✏️ update_profile_text"]
        Diagnostics["🧭 lead_diagnostics"]
        Geo["📍 geo_coverage_checker"]
    end

    HumanAgent["👩‍💼 Human Agent<br>(Escalation Support)"]

    User -->|🔊 “Why no leads lately?”| MainAgent
    MainAgent <--> Metrics
    MainAgent <--> Ratings
    MainAgent <--> ResponseTime
    MainAgent <--> Diagnostics
    Diagnostics <--> Rewrite
    MainAgent --> Geo
    MainAgent -->|🗣️ Spoken response| User

    MainAgent -->|🚨 Handoff if user asks for help or gets stuck| HumanAgent
    HumanAgent -->|📞 Callback or follow-up| User
