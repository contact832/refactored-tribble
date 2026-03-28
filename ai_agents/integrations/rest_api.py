"""API REST pour contrôler les agents via HTTP."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ai_agents.core.orchestrator import OrchestratorAgent


def create_api_blueprint(orchestrator: OrchestratorAgent) -> Blueprint:
    """Crée un blueprint Flask pour l'API REST des agents."""
    api = Blueprint("api", __name__, url_prefix="/api")

    @api.route("/task", methods=["POST"])
    def run_task():
        data = request.get_json(force=True)
        task = data.get("task", "")
        context = data.get("context", {})

        if not task:
            return jsonify({"error": "Le champ 'task' est requis."}), 400

        result = orchestrator.run(task, context)
        return jsonify({"response": result})

    @api.route("/status", methods=["GET"])
    def get_status():
        return jsonify(orchestrator.get_status())

    @api.route("/memory", methods=["GET"])
    def get_memory():
        """Voir la memoire de chaque agent."""
        memory = {}
        for name, agent in orchestrator.sub_agents.items():
            memory[name] = {
                "messages": len(agent.conversation_history),
                "history": agent.conversation_history[-4:],  # 2 derniers echanges
            }
        return jsonify(memory)

    @api.route("/memory/clear", methods=["POST"])
    def clear_memory():
        """Vider la memoire de tous les agents."""
        for agent in orchestrator.sub_agents.values():
            agent.conversation_history.clear()
        return jsonify({"status": "Memoire videe pour tous les agents"})

    return api
