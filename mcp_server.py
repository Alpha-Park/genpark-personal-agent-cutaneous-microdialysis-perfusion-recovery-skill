"""
MCP Server for Cutaneous Microdialysis Perfusion Recovery Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import CutaneousMicrodialysisClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cutaneous-microdialysis-perfusion-recovery-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "zero_net_flux_calibration",
                        "description": "Calculate true interstitial extracellular concentration and in vivo probe extraction fraction via zero-net-flux regression.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "trials": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                        "maxItems": 2
                                    },
                                    "description": "List of [C_in, C_out] pairs in umol/L."
                                },
                                "analyte_name": {"type": "string", "description": "Name of analyte (e.g. Glucose, Lactate, Histamine)."},
                                "membrane_cutoff_kda": {"type": "number", "description": "Membrane molecular weight cut-off in kDa (default: 20.0)."}
                            },
                            "required": ["trials"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "zero_net_flux_calibration":
            cutoff = float(args.get("membrane_cutoff_kda", 20.0))
            client = CutaneousMicrodialysisClient(membrane_cutoff_kda=cutoff)
            raw_trials = args.get("trials", [])
            trials_tuples = [(float(t[0]), float(t[1])) for t in raw_trials]
            analyte = args.get("analyte_name", "Analyte")
            try:
                res = client.zero_net_flux_calibration(trials_tuples, analyte_name=analyte)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
