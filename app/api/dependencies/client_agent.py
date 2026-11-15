from fastapi import Request

from app.agents.client.agent import ClientAgent


def get_client_agent(request: Request) -> ClientAgent:
    return request.app.state.client_agent