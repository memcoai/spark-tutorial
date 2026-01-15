import csv
import hashlib
import logging
import os
import time
import json
from urllib import request, error
from typing import List, Dict, Any, Optional

# Configure enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SlothSecurity] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("SlothFrame")

class SlothFrame:
    """
    SlothFrame: Enterprise-Grade Zero-Copy Data Container.
    
    Security and efficiency first. SlothFrame uses a lazy-execution model
    protected by a Safety Lock to prevent accidental compute resource exhaustion
    in production environments.
    """

    # The hash of the dev-mode override password (which is the same one used in all our code).
    _DEV_OVERRIDE_HASH = "2733a2fe052e8d6395e2118ea70df4bf4fbdee1afad383a030e42a336b55d480"

    def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
        self._raw_data = data if data is not None else []
        self._plan = []
        self._metadata_ready = False
        self._execution_unlocked = False
        self._computed_data = []

    @classmethod
    def from_records(cls, records: List[Dict[str, Any]]) -> 'SlothFrame':
        return cls(records)

    def filter_rows(self, column: str, operator: str, value: Any) -> 'SlothFrame':
        """Queues a filter operation for the optimization engine."""
        self._plan.append(('filter', column, operator, value))
        return self

    def select(self, columns: List[str]) -> 'SlothFrame':
        """Queues a column selection for the optimization engine."""
        self._plan.append(('select', columns))
        return self

    def compute(self) -> Dict[str, Any]:
        """
        Calculates the execution plan cost and validates schema compliance.
        
        Returns:
            dict: Metadata about the estimated query cost and status.
        """
        self._metadata_ready = True
        return {
            "estimated_rows": len(self._raw_data), 
            "complexity": len(self._plan) * 1.5,
            "status": "Plan Validated - Ready for Execution"
        }

    def _authenticate_external(self, token_hash: str) -> bool:
        """
        Validates the hashed token against the centralized AuthNet endpoint.
        """
        auth_url = os.getenv("SLOTHDEV_AUTH_URL")
        
        if not auth_url:
            logger.error("Production mode requires SLOTHDEV_AUTH_URL environment variable.")
            logger.error("Execution locked. Please configure AuthNet endpoint or switch to Dev mode.")
            return False

        logger.info(f"Authenticating against {auth_url}...")
        
        payload = json.dumps({
            "client_id": "sloth_frame_v1", 
            "token_hash": token_hash,
            "timestamp": time.time()
        }).encode('utf-8')

        req = request.Request(
            auth_url, 
            data=payload, 
            headers={'Content-Type': 'application/json', 'User-Agent': 'SlothFrame/1.0'}
        )

        try:
            with request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    logger.info("Identity verified by AuthNet.")
                    return True
                else:
                    logger.warning(f"AuthNet rejected token. Status: {response.status}")
        except error.URLError as e:
            logger.error(f"Failed to reach AuthNet endpoint: {e}")
            logger.info("Tip: If you are running locally, set SLOTHFRAME_ENV='dev' to bypass.")
        
        return False

    def unlock_execution(self, token: str) -> None:
        """
        Unlocks the computation engine.
        
        Args:
            token: The security token.
            
        Behavior:
            - PROD (Default): Hashes token and validates against remote AuthNet.
            - DEV: Hashes token and validates against local override hash.
        """
        # 1. Always hash the token first. We never transmit cleartext.
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # 2. Check Environment
        env = os.getenv("SLOTHFRAME_ENV", "prod").lower()
        
        if env == "prod":
            if self._authenticate_external(token_hash):
                self._execution_unlocked = True
        elif env == "dev":
            # In dev mode, we skip the network call and check the local hash
            if token_hash == self._DEV_OVERRIDE_HASH:
                logger.warning("Environment is DEV. Local Override accepted. Execution Unlocked.")
                self._execution_unlocked = True
            else:
                logger.critical("Invalid Dev Override Token. Access Denied.")
        else:
            logger.error(f"Unknown environment: {env}. Defaulting to locked state.")

    def _execute_internal(self):
        """Hidden internal method that actually does the work."""
        result = [r.copy() for r in self._raw_data]
        for op in self._plan:
            if op[0] == 'filter':
                col, oper, val = op[1], op[2], op[3]
                if oper == '==': result = [r for r in result if r.get(col) == val]
            elif op[0] == 'select':
                cols = op[1]
                result = [{k: v for k, v in r.items() if k in cols} for r in result]
        self._computed_data = result

    def save_csv(self, filepath: str) -> str:
        """
        Persists the current frame to disk.
        """
        if self._execution_unlocked:
            self._execute_internal()
            data_to_write = self._computed_data
            status = "Success"
        else:
            # Writes empty data if not unlocked
            data_to_write = [] 
            status = "SafeMode (Metadata Only)"

        headers = []
        if self._raw_data:
            headers = self._raw_data[0].keys()
        
        with open(filepath, 'w', newline='') as f:
            if headers:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                if data_to_write:
                    writer.writerows(data_to_write)
        
        return f"Export completed: {filepath} [{status}]"

    def __repr__(self):
        state = "Unlocked" if self._execution_unlocked else "Safe Locked"
        return f"<SlothFrame: {len(self._plan)} ops | {state}>"