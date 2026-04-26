import os
import sys
import hashlib
import re

class NEXA_Sovereign_Engine:
    def __init__(self):
        self.key_file = "key.nx"
        self.storage = {}
        self.vault = {}
        self.original_data = {}
        self.vault_mode = False
        
        # أهم خطوة: قفل النظام إذا ما فيه مفتاح
        self._boot_lock()

    def _boot_lock(self):
        # التحقق من وجود الملف
        if not os.path.exists(self.key_file):
            print("\n" + "!"*45)
            print("[NXC]: FATAL ERROR - SOVEREIGN KEY MISSING")
            print("[NXC]: SYSTEM LOCKED. PLEASE INSERT 'key.nx'")
            print("!"*45 + "\n")
            sys.exit() # يخرج من البرنامج فوراً

        # التحقق من النص اللي داخل الملف
        with open(self.key_file, "r") as f:
            content = f.read().strip()
            if content != "NEXA_9922_ORIGINAL":
                print("\n[NXC]: SECURITY BREACH - INVALID KEY")
                print("[NXC]: ACCESS DENIED.")
                sys.exit()
        
        print("[NXC]: KEY AUTHENTICATED. SOVEREIGN MODE ACTIVE.\n")

    def execute(self, script):
        for line in script.split('\n'):
            line = line.strip()
            if not line or line.startswith("//"): continue
            
            # منطق الخزنة (Vault)
            if "open vault:" in line:
                self.vault_mode = True
                continue
            if line == "}":
                self.vault_mode = False
                continue

            # التعيين (Set)
            if "set" in line and "->" in line:
                parts = re.match(r'set\s+(\w+)\s*->\s*(.*)', line)
                if parts:
                    name, val = parts.groups()
                    val = val.strip().strip('"')
                    if self.vault_mode:
                        self.vault[name] = hashlib.sha256(val.encode()).hexdigest()[:12]
                        self.original_data[name] = val
                    else:
                        self.storage[name] = val

            # الطباعة (Say) مع حماية الخزنة
            elif "io.say" in line:
                target_match = re.search(r'\((.*)\)', line)
                if target_match:
                    target = target_match.group(1)
                    if target in self.vault:
                        print(f"\033[91m[NEXA]: Logic violation at '{target}'. Respect the Vault!\033[0m")
                    else:
                        print(f"NX_Output: {self.storage.get(target, target)}")

            # الكشف (Reveal)
            if line.startswith("reveal vault:"):
                print(f"\n\033[92m--- [NXC]: REVEALING SOVEREIGN DATA ---\033[0m")
                for k, v in self.original_data.items():
                    print(f"[UNLOCKED]: {k} -> {v}")

# --- تشغيل المحرك ---
if __name__ == "__main__":
    nexa = NEXA_Sovereign_Engine()
    
    # حط كودك هنا لتجربته
    nexa.execute("// System Ready")
