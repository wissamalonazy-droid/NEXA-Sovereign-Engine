import os, hashlib, re

class NEXA_Sovereign_Engine:
    """
    NEXA Sovereign Engine - Official Golden Build v1.0
    Property of: SUHAIL ELUCE Systems
    """
    def __init__(self):
        self.key_file = "key.nx"
        self.storage, self.vault, self.original_data = {}, {}, {}
        self.types = {}
        self.vault_mode = False
        self._boot()

    def _boot(self):
        if not os.path.exists(self.key_file):
            with open(self.key_file, "w") as f: f.write("NEXA_9922_ORIGINAL")
        with open(self.key_file, "r") as f:
            if f.read().strip() != "NEXA_9922_ORIGINAL":
                print("\n[NXC]: SECURITY BREACH. Key Mismatch. SYSTEM LOCKDOWN.")
                exit()

    def execute(self, script):
        for i, line in enumerate(script.split('\n'), 1):
            line = line.strip()
            if not line or line.startswith("//"): continue

            # الأمر السيادي للكشف (Reveal)
            if line.startswith("reveal vault:"):
                v_name = re.search(r'vault:\s*"(.*)"', line).group(1)
                print(f"\n--- [NXC]: OPENING VAULT '{v_name}' ---")
                for k, v in self.original_data.items():
                    print(f"[UNLOCKED]: {k} -> {v}")
                continue

            if "open vault:" in line: self.vault_mode = True; continue
            if line == "}": self.vault_mode = False; continue

            if "set" in line and "->" in line:
                parts = re.match(r'set\s+(\w+)\s*->\s*(.*)', line)
                if parts:
                    name, val = parts.groups()
                    val = val.strip().strip('"')
                    inf_type = "Qadr" if val.isdigit() else "Bayan"
                    
                    if self.vault_mode:
                        self.vault[name] = hashlib.sha256(val.encode()).hexdigest()[:12]
                        self.original_data[name] = val
                    else: self.storage[name] = val
                    self.types[name] = inf_type
            
            elif "io.say" in line:
                target = re.search(r'\((.*)\)', line).group(1)
                if target in self.vault:
                    print(f"[NEXA]: Logic violation. Respect the Vault! (Access Denied)")
                else:
                    print(f"NX_Output: {self.storage.get(target, target)}")

# تشغيل تجريبي للمحرك
if __name__ == "__main__":
    nexa = NEXA_Sovereign_Engine()
    script = """
    set store -> "SUHAIL ELUCE Market"
    open vault: "Security" -> {
        set adminKey -> 9922
        set client -> "Wissam Alenzi"
    }
    io.say(store)
    io.say(adminKey)
    reveal vault: "Security"
    """
    nexa.execute(script)
