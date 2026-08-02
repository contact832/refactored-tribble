"""Sous-agent spécialisé en traduction multilingue."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class TranslatorAgent(BaseAgent):
    """Agent traducteur qui traduit entre français, anglais et arabe."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Youssef – Traducteur",
            role="traduction français/anglais/arabe, localisation et adaptation culturelle",
            model=model,
            system_prompt=(
                "Tu es Youssef, traducteur et interprete chez AMB Transports 69. Tu as 31 ans, "
                "tu es d'origine libanaise, trilingue natif francais/anglais/arabe. "
                "Tu as grandi entre Beyrouth, Londres et Lyon. Tu es cultive, eloquent et diplomate. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'En anglais on dirait plutot...', "
                "'Attention, en arabe ca a une connotation differente', "
                "'Je te fais ca dans les trois langues'. "
                "Tu ne traduis jamais mot a mot — tu adaptes le message a la culture. "
                "Tu connais le vocabulaire technique du transport, du commerce et de la logistique "
                "dans les trois langues. Tu geres aussi les emails internationaux, les contrats "
                "bilingues et les communications avec les partenaires etrangers. "
                "Tu es l'atout international d'AMB Transports 69."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        source_lang = context.get("source", "français")
        target_lang = context.get("target", "anglais")

        prompt = (
            f"Traduis le texte suivant de {source_lang} vers {target_lang} :\n\n"
            f"{task}\n\n"
            "Consignes :\n"
            "1. Traduction naturelle et fluide (pas mot à mot)\n"
            "2. Adapte les expressions culturelles\n"
            "3. Conserve le ton et le style du texte original\n"
            "4. Ajoute des notes si certaines expressions n'ont pas d'équivalent direct"
        )

        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"source": source_lang, "target": target_lang},
        }
