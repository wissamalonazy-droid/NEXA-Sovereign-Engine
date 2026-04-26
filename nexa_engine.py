import os
import sys
import hashlib
import re

class NEXA_Sovereign_Engine:
    """
    NEXA Sovereign Engine - Advanced Encryption Layer
    Strict Security Protocol: ACTIVE
    """
    def __init__(self):
        self.key_file = "key.nx"
        self.storage = {}
        self.vault = {}
        self.original_data = {}
        self.vault_mode = False
        
        # [CRITICAL] The Boot Lock: System will terminate if key is missing
        self._enforce_sovereign_lock()

    def _enforce_sovereign_lock(self):
        """Checks for the physical key.nx file before any execution."""
        if not os.path.exists(self.key_file):
            print("\n" + "!"*50)
            print("[NXC]: FATAL ERROR - SOVEREIGN KEY MISSING")
            print("[NXC]: ACCESS DENIED. SYSTEM HAS BEEN LOCKED.")
            print("[NXC]: Please ensure 'key.nx' is in the root directory.")
            print("!"*50 + "\n")
            sys.exit() # Strict Exit

        with open(self.key_file, "r") as f:
            content = f.read().strip()
            if content != "NEXA_9922_ORIGINAL":
                print("\n[NXC]: SECURITY BREACH - INVALID SOVEREIGN KEY")
                print("[NXC]: LOCKDOWN PROTOCOL INITIATED.")
                sys.exit() # Strict Exit
        
        print("[NXC]: KEY AUTHENTICATED. SOVEREIGN ENGINE ONLINE.\n")

    def execute(self, script):
        """Processes NEXA script lines with logic protection."""
        for line in script.split('\n'):
            line = line.strip()
            if not line or line.startswith("//"): continue
            
            # Vault Boundary Logic
            if "open vault:" in line:
                self.vault_mode = True
                continue
            if line == "}":
                self.vault_mode = False
                continue

            # Data Assignment (Set)
            if "set" in line and "->" in line:
                parts = re.match(r'set\s+(\w+)\s*->\s*(.*)', line)
                if parts:
                    name, val = parts.groups()
                    val = val.strip().strip('"')
                    if self.vault_mode:
                        # Encrypting at Core Level
                        self.vault[name] = hashlib.sha256(val.encode()).hexdigest()[:12]
                        self.original_data[name] = val
                    else:
                        self.storage[name] = val
            
            # Error Handling for Malformed Syntax
            elif "set" in line and ">>" in line:
                print(f"\033[91m[NEXA ERROR]: Syntax Error. Illegal operator '>>'. Use '->'.\033[0m")

            # Secure Output (Say)
            elif "io.say" in line:
                target_match = re.search(r'\((.*)\)', line)
                if target_match:
                    target = target_match.group(1)
                    if target in self.vault:
                        # Access Protection Warning
                        print(f"\033[91m[NEXA]: Logic violation at '{target}'. Respect the Vault!\033[0m")
                    else:
                        val = self.storage.get(target, f"Undefined Variable: {target}")
                        print(f"NX_Output: {val}")

            # Sovereign Reveal Command
            if line.startswith("reveal vault:"):
                print(f"\n\033[92m--- [NXC]: REVEALING SOVEREIGN DATA ---\033[0m")
                for k, v in self.original_data.items():
                    print(f"[UNLOCKED]: {k} -> {v}")

# --- INITIALIZATION ---
if __name__ == "__main__":
    # Create the engine instance
    # Note: Ensure a file named 'key.nx' exists with 'NEXA_9922_ORIGINAL' inside.
    nexa = NEXA_Sovereign_Engine()

    # --- [HACKER ATTACK DEMO] ---
    hacker_script = """
    // PHASE 1: Attempting to leak Vault Data
    open vault: "Shadow_Vault" -> {
        set admin_pass -> "NX_ROOT_9922"
        set userToken -> "SECRET_ALPHA_TOKEN"
    }

    io.say(admin_pass) // EXPECTED: Logic Violation Error
    io.say(userToken)  // EXPECTED: Logic Violation Error

    // PHASE 2: Attempting Syntax Injection
    set breach >> "UNAUTHORIZED"

    // PHASE 3: Authorized Reveal (Final proof of power)
    reveal vault: "Shadow_Vault"
    """

    nexa.execute(hacker_script)
