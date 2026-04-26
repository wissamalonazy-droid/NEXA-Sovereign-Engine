import os
import sys
import hashlib
import re

class NEXA_Sovereign_Engine:
    def __init__(self):
        self.key_file = "key.nx"
        # --- [السطر الانتحاري] ---
        self._ensure_key_exists() 
        
        self.storage = {}
        self.vault = {}
        self.original_data = {}
        self.vault_mode = False

    def _ensure_key_exists(self):
        # التحقق الصارم: إذا الملف مو موجود في المجلد، اخرج فوراً
        if not os.path.exists(self.key_file):
            print("\n" + "!"*40)
            print("[NXC]: FATAL ERROR - SOVEREIGN KEY MISSING")
            print("[NXC]: SYSTEM LOCKED FOR SECURITY")
            print("!"*40 + "\n")
            sys.exit() # ينهي تشغيل البرنامج كلياً

        # إذا الملف موجود، تأكد من الكلام اللي داخله
        with open(self.key_file, "r") as f:
            if f.read().strip() != "NEXA_9922_ORIGINAL":
                print("\n[NXC]: SECURITY BREACH - INVALID KEY")
                sys.exit()
        
        print("[NXC]: ACCESS GRANTED. WELCOME WISSAM.\n")

    def execute(self, script):
        # (باقي كود التنفيذ اللي أعطيتك اياه سابقاً)
        for line in script.split('\n'):
            line = line.strip()
            if not line or line.startswith("//"): continue
            if "open vault:" in line: self.vault_mode = True; continue
            if line == "}": self.vault_mode = False; continue
            if "set" in line and "->" in line:
                parts = re.match(r'set\s+(\w+)\s*->\s*(.*)', line)
                if parts:
                    name, val = parts.groups()
                    val = val.strip().strip('"')
                    if self.vault_mode:
                        self.vault[name] = hashlib.sha256(val.encode()).hexdigest()[:12]
                        self.original_data[name] = val
                    else: self.storage[name] = val
            elif "io.say" in line:
                target_match = re.search(r'\((.*)\)', line)
                if target_match:
                    target = target_match.group(1)
                    if target in self.vault: print(f"[NEXA]: Logic violation at '{target}'.")
                    else: print(f"NX_Output: {self.storage.get(target, target)}")
            if line.startswith("reveal vault:"):
                print(f"\n--- [REVEALING] ---")
                for k, v in self.original_data.items(): print(f"[UNLOCKED]: {k} -> {v}")

# --- تجربة القفل ---
if __name__ == "__main__":
    nexa = NEXA_Sovereign_Engine()
    test_code = 'set x -> "Test"\nio.say(x)'
    nexa.execute(test_code)
