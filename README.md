# Docker Insights Agent - Hackathon Project

🤖 AI-powered conversational interface for Docker security insights using real Scout data.

## What This Does
- Connects to Docker Scout API for real security data
- Provides conversational interface for insights (92 critical vulns, 500+ policy violations)
- Ready for hackathon demo with extensible foundation

## Quick Start
1. **Prerequisites**: `brew install git go go-task node python`
2. **Get cagent**: `git clone https://github.com/docker/cagent.git && cd cagent && task build`
3. **Clone this repo**: `git clone https://github.com/etugarinova/docker-insights-agent.git`
4. **Copy files**: `cp docker-insights-agent/* cagent/`
5. **Set API key**: `export OPENAI_API_KEY=your_key_here`
6. **Run**: `./bin/cagent run docker-insights-simple.yaml`

## Demo Questions
- "What's our current security posture?"
- "What are the most critical issues we need to fix?"
- "Show me our policy violations"

## Files
- `docker-insights-simple.yaml` - **Main agent** (works now!)
- `docker-insights-mcp/simple_server.py` - Real Scout API integration
- `docker-insights-agent.yaml` - MCP version (future)
