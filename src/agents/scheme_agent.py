"""Government-scheme eligibility agent (Challenge 3 everyday impact)."""
from __future__ import annotations

from src.agents.base import Agent
from src.agents.grounding import ground
from src.contracts import AgentResult, AgentTask, ProposedAction

MOCK_FARMERS = {
    "ramesh": {
        "name": "Ramesh Kumar",
        "landholding_hectares": 1.5,
        "income_tax_payer": False,
        "is_govt_employee": False,
    },
    "suresh": {
        "name": "Suresh Patel",
        "landholding_hectares": 0.0,
        "income_tax_payer": False,
        "is_govt_employee": False,
    },
    "anil": {
        "name": "Anil Sharma",
        "landholding_hectares": 3.0,
        "income_tax_payer": True,
        "is_govt_employee": False,
    },
    "vijay": {
        "name": "Vijay Singh",
        "landholding_hectares": 2.5,
        "income_tax_payer": False,
        "is_govt_employee": True,
    },
}


class SchemeAgent(Agent):
    name = "scheme_agent"
    domain = "govt_scheme"

    def __init__(self) -> None:
        self.draft_applications: list[dict] = []

    def can_handle(self, task: AgentTask) -> bool:
        return task.intent in {"check_scheme", "apply_scheme"}

    def run(self, task: AgentTask) -> AgentResult:
        scheme = task.params.get("scheme", "pmkisan")
        citation = ground(scheme)
        if citation is None:
            return AgentResult(answer=f"Unknown scheme '{scheme}'.")

        applicant_key = task.params.get("applicant", "").lower()

        if scheme == "pmkisan":
            if applicant_key in MOCK_FARMERS:
                farmer = MOCK_FARMERS[applicant_key]
                if farmer["landholding_hectares"] <= 0:
                    status = "Ineligible"
                    reason = "Applicant is landless (PM-KISAN requires cultivable landholding)."
                elif farmer["income_tax_payer"]:
                    status = "Ineligible"
                    reason = "Applicant paid income tax in last assessment year (exclusion criteria)."
                elif farmer["is_govt_employee"]:
                    status = "Ineligible"
                    reason = "Applicant is a government employee (exclusion criteria)."
                else:
                    status = "Eligible"
                    reason = f"Applicant has cultivable land ({farmer['landholding_hectares']} ha), is non-taxpayer, and non-govt employee."

                if status == "Eligible":
                    answer = f"Checking PM-KISAN eligibility for {farmer['name']}: {status}. {reason} {citation.snippet}"
                else:
                    answer = f"Checking PM-KISAN eligibility for {farmer['name']}: {status}. Reason: {reason}"
            else:
                status = "Information Requested"
                answer = f"PM-KISAN Scheme: {citation.snippet} Please specify a valid applicant profile (e.g. Ramesh, Suresh, Anil, Vijay) for verification."
        else:
            # Ayushman Bharat
            status = "Eligible"
            answer = f"Checking Ayushman Bharat (PM-JAY) eligibility: Eligible. (Low-income socio-economic census household). {citation.snippet}"

        action = None
        # Only propose application if applicant is eligible or if general information is requested (we allow submission draft for testing)
        if task.intent == "apply_scheme" and status != "Ineligible":
            name_val = MOCK_FARMERS.get(applicant_key, {}).get("name", applicant_key or "Applicant")
            action = ProposedAction(
                description=f"Submit draft application for {citation.title} for {name_val}",
                domain=self.domain,
                reversible=True,
                citations=[citation],
                payload={"scheme": scheme, "applicant": applicant_key},
            )

        return AgentResult(answer=answer, citations=[citation], proposed_action=action)

    def execute(self, payload: dict) -> None:
        self.draft_applications.append(payload)

    def undo(self, payload: dict) -> None:
        if payload in self.draft_applications:
            self.draft_applications.remove(payload)
