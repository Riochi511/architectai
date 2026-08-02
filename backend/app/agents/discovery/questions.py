from app.agents.discovery.schemas import DiscoveryStage


DISCOVERY_QUESTIONS = {
    DiscoveryStage.VISION: [
        "What problem are you trying to solve?"
    ],

    DiscoveryStage.USERS: [
        "Who will use this system?"
    ],

    DiscoveryStage.PROBLEM: [
        "Describe the biggest pain point your users experience today."
    ],

    DiscoveryStage.FUNCTIONAL: [
        "What are the core features this system must have?"
    ],

    DiscoveryStage.NON_FUNCTIONAL: [
        "Are there any performance, security, or scalability requirements?"
    ],

    DiscoveryStage.AI: [
        "Which parts of this system should use AI?"
    ],

    DiscoveryStage.DATA: [
        "What data will the AI need?"
    ],

    DiscoveryStage.CONSTRAINTS: [
        "Are there any technical or business constraints?"
    ],

    DiscoveryStage.DEPLOYMENT: [
        "Where do you plan to deploy this system?"
    ],
}