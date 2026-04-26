import os
import hashlib
import re
import sys

class NEXA_Sovereign_Engine:
    """
    NEXA Sovereign Engine - Hardened Build v1.1
    Security Status: STRICT MODE
    """
    def __init__(self):
        self.key_file = "key.nx"
        self.storage = {}
        self.vault = {}
        self.original_data = {}
        self.vault_mode = False
        # التحقق من القفل عند التشغيل مباشرة
        self._boot_sequence()

    def _boot_sequence(self):
        print("--- [NXC]: INITIALIZING SOVEREIGN CORE ---")
        
        # 1. التحقق من وجود الملف (لن يصنع ملفاً جديداً بعد الآن)
        if not os.path.exists(self.key_file):
            print("\n[NXC]: FATAL ERROR. Sovereign Key ('key.nx') is missing.")
            print("[NXC]: Access Denied. System Locked.")
            sys.exit() # إغلاق البرنامج فوراً

        # 2. التحقق من صحة المفتاح داخل الملف
        with open(self.key_file, "r") as f:
            user_key = f.read().strip()
            if user_key != "NEXA_9922_ORIGINAL":
                print("\n[NXC]: SECURITY BREACH. Invalid Secret Key detected.")
                print("[NXC]: System Lockdown Initiated.")
                sys.exit()
        
        print("[NXC]: Key Authenticated. System Ready.\n")

    def execute(self, script):
        for line in script.split('\n'):
            line = line.strip()
            if not line or line.startswith("//"): continue

            # أمر الكشف (Reveal)
            if line.startswith("reveal vault:"):
                v_match = re.search(r'vault:\s*"(.*)"', line)
                if v_match:
                    v_name = v_match.group(1)
                    print(f"\n--- [NXC]: REVEALING VAULT '{v_name}' ---")
                    for k, v in self.original_data.items():
                        print(f"[UNLOCKED]: {k} -> {v}")
                continue

            # أوامر الخزانة
            if "open vault:" in line:
                self.vault_mode = True
                continue
            if line == "}":
                self.vault_mode = False
                continue

            # أوامر التعيين (Set)
            if "set" in line and "->" in line:
                parts = re.match(r'set\s+(\w+)\s*->\s*(.*)', line)
                if parts:
                    name, val = parts.groups()
                    val = val.strip().strip('"')
                    
                    if self.vault_mode:
                        # تشفير البيانات داخل الخزانة
                        self.vault[name] = hashlib.sha256(val.encode()).hexdigest()[:12]
                        self.original_data[name] = val
                    else:
                        self.storage[name] = val

            # أوامر الطباعة (Say)
            elif "io.say" in line:
                target_match = re.search(r'\((.*)\)', line)
                if target_match:
                    target = target_match.group(1)
                    if target in self.vault:
                        print(f"[NEXA]: Logic violation at '{target}'. Respect the Vault!")
                    else:
                        print(f"NX_Output: {self.storage.get(target, target)}")

# --- [تجربة النظام] ---
if __name__ == "__main__":
    nexa = NEXA_Sovereign_Engine()
    
    # هذا الكود لن يعمل إلا إذا كان ملف key.nx موجوداً وصحيحاً
    clean_code = """
    set system -> "NEXA CORE"
    open vault: "Security" -> {
        set masterKey -> 9922
    }
    io.say(system)
    io.say(masterKey)
    reveal vault: "Security"
    """
    nexa.execute(clean_code)
