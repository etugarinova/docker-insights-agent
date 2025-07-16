#!/usr/bin/env python3
import json
import subprocess
import requests
import sys

def get_docker_token():
    """Get Docker authentication token"""
    try:
        result = subprocess.run([
            'docker-credential-desktop', 'get'
        ], input='https://index.docker.io/v1/access-token', 
           text=True, capture_output=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('Secret')
    except Exception as e:
        print(f"Error getting token: {e}")
    return None

def get_security_insights(organization="docker", stream="environment:production"):
    """Get security insights from Docker Scout"""
    
    token = get_docker_token()
    if not token:
        return {"error": "Could not get Docker authentication token"}
    
    query = """
    query ($organization: String!, $stream: String!) {
      goalResultSummaries(context: {organization: $organization}, query: {stream: $stream}) {
        items {
          stream
          policy {
            displayName
          }
          totalDeviations
          totalImages
        }
      }
      streamVulnerabilityReports(context: {organization: $organization}, query: {stream: $stream}) {
        items {
          timestamp
          vulnerabilityReport {
            critical
            high
            medium
            low
          }
        }
      }
      cvesByStream(context: {organization: $organization}, query: {stream: $stream, paging: {pageSize: 10}}) {
        paging {
          totalCount
        }
        items {
          cveId
          highestSeverity
          detectedInCount
        }
      }
    }
    """
    
    try:
        response = requests.post(
            "https://api.scout.docker.com/v1/graphql",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "query": query,
                "variables": {"organization": organization, "stream": stream}
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}: {response.text}"}
            
    except Exception as e:
        return {"error": f"Error calling Scout API: {e}"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test the function
        result = get_security_insights()
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python3 simple_server.py test")
