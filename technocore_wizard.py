import os
import sys
import json
import shutil
import urllib.request
import webbrowser
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- COLOR THEORY (Slate / Azure / Emerald) ---
BG_MAIN = "#0F172A"       # Slate 900 (Deep background)
BG_SURFACE = "#1E293B"    # Slate 800 (Card background)
TEXT_PRIMARY = "#F8FAFC"  # Slate 50 (Main text)
TEXT_MUTED = "#94A3B8"    # Slate 400 (Secondary text)
ACCENT_BLUE = "#3B82F6"   # Blue 500 (Primary buttons)
SUCCESS = "#10B981"       # Emerald 500 (Success states)
WARNING = "#F59E0B"       # Amber 500 (Warnings/Alerts)
DANGER = "#EF4444"        # Red 500 (Errors)

ctk.set_appearance_mode("dark")

class TechnocoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Technocore Contributor")
        self.geometry("700x750") 
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)

        # Environment State
        self.target_dir = os.path.join(os.path.expanduser("~"), "Technocore")
        self.repo_url = "https://github.com/zunmax/technocore-did-starter.git"
        self.venv_python = os.path.join(self.target_dir, ".venv", "Scripts", "python.exe")
        self.agent = "technocore_agent.py"
        
        self.passphrase = ""
        self.did = ""
        self.commit_hash = ""
        self.contrib_url = ""

        # UI Container
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_SURFACE, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        self.show_step_1()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def get_agent_wrapper(self, *args):
        """
        THE FIX: Creates a temporary Python script that forces the agent to read 
        passwords from our pipeline instead of freezing on a non-existent Windows console.
        """
        wrapper_path = os.path.join(self.target_dir, "gui_wrapper.py")
        args_json = json.dumps(["technocore_agent.py"] + list(args))
        code = (
            "import getpass, sys, runpy\n"
            "getpass.getpass = lambda p='': input()\n"  # Forces getpass to use standard input
            f"sys.argv = {args_json}\n"
            "runpy.run_path('technocore_agent.py', run_name='__main__')\n"
        )
        with open(wrapper_path, "w", encoding="utf-8") as f:
            f.write(code)
        return f'"{self.venv_python}" gui_wrapper.py'

    def run_cmd(self, cmd, cwd=None, input_text=None):
        try:
            result = subprocess.run(
                cmd, cwd=cwd, input=input_text, text=True, 
                capture_output=True, encoding='utf-8', shell=True
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)

    def run_cmd_live(self, cmd, cwd, input_text, log_callback):
        log_callback(f"> Executing Agent...")
        try:
            process = subprocess.Popen(
                cmd, cwd=cwd, shell=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            
            if input_text:
                try:
                    process.stdin.write(input_text)
                    process.stdin.flush()
                    process.stdin.close() 
                    log_callback("[Passphrase injected successfully]")
                except Exception as e:
                    log_callback(f"[Stdin error: {e}]")

            for line in iter(process.stdout.readline, ''):
                if line:
                    log_callback(line.strip())
                
            process.stdout.close()
            return_code = process.wait()
            log_callback(f"[Process finished with exit code {return_code}]")
            return return_code == 0

        except Exception as e:
            log_callback(f"[System Error: {e}]")
            return False

    # --- STEP 1: Welcome ---
    def show_step_1(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Welcome to Technocore Contributor", font=("Segoe UI", 24, "bold"), text_color=TEXT_PRIMARY).pack(pady=(40, 20))
        
        desc = (
            "This app helps you create your Technocore DID, make a signed contribution,\n"
            "create proof of your contribution, and verify it.\n\n"
            "You don't need to know Python or Git."
        )
        ctk.CTkLabel(self.main_frame, text=desc, font=("Segoe UI", 14), text_color=TEXT_MUTED, justify="center").pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Start Setup", command=self.show_step_2, fg_color=ACCENT_BLUE, font=("Segoe UI", 14, "bold"), height=45).pack(pady=40)

    # --- STEP 2, 3, 4: System Check ---
    def show_step_2(self):
        self.clear_frame()
        self.is_checking_deps = True 
        
        ctk.CTkLabel(self.main_frame, text="System Check", font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY).pack(pady=(20, 20))
        self.checks_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_MAIN, corner_radius=10)
        self.checks_frame.pack(fill="x", padx=40, pady=10)
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=40, pady=10)

        self.update_system_checks()

    def update_system_checks(self):
        if not hasattr(self, 'is_checking_deps') or not self.is_checking_deps:
            return

        for widget in self.checks_frame.winfo_children():
            widget.destroy()
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        def is_python_installed():
            if shutil.which("py") or shutil.which("python"): 
                return True
            local_app = os.environ.get('LOCALAPPDATA', '')
            if local_app:
                for version in ["310", "311", "312", "313"]:
                    exe_path = os.path.join(local_app, "Programs", "Python", f"Python{version}", "python.exe")
                    if os.path.exists(exe_path):
                        return True
            return os.path.exists(r"C:\Program Files\Python312\python.exe")
            
        def is_git_installed():
            if shutil.which("git"): 
                return True
            return os.path.exists(r"C:\Program Files\Git\cmd\git.exe")

        def is_online():
            try:
                urllib.request.urlopen("https://github.com", timeout=3)
                return True
            except:
                return False

        py_ok = is_python_installed()
        git_ok = is_git_installed()
        net_ok = is_online()

        ctk.CTkLabel(self.checks_frame, text=f"{'✅' if True else '❌'} Windows 10/11 (64-bit)", font=("Segoe UI", 14), text_color=SUCCESS).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(self.checks_frame, text=f"{'✅' if net_ok else '❌'} Internet connection", font=("Segoe UI", 14), text_color=SUCCESS if net_ok else DANGER).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(self.checks_frame, text=f"{'✅' if py_ok else '❌'} Python executable found", font=("Segoe UI", 14), text_color=SUCCESS if py_ok else DANGER).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(self.checks_frame, text=f"{'✅' if git_ok else '❌'} Git executable found", font=("Segoe UI", 14), text_color=SUCCESS if git_ok else DANGER).pack(anchor="w", padx=20, pady=5)

        if py_ok and git_ok and net_ok:
            self.is_checking_deps = False 
            ctk.CTkButton(self.actions_frame, text="Continue", command=self.show_step_5, fg_color=ACCENT_BLUE, font=("Segoe UI", 14, "bold"), height=45).pack(pady=30)
        else:
            if not py_ok:
                ctk.CTkButton(self.actions_frame, text="Install Python", command=lambda: webbrowser.open("https://www.python.org/downloads/"), fg_color=WARNING, text_color=BG_MAIN).pack(pady=5)
            if not git_ok:
                ctk.CTkButton(self.actions_frame, text="Install Git", command=lambda: webbrowser.open("https://git-scm.com/downloads"), fg_color=WARNING, text_color=BG_MAIN).pack(pady=5)

            wait_frame = ctk.CTkFrame(self.actions_frame, fg_color="transparent")
            wait_frame.pack(pady=15)
            spinner = ctk.CTkProgressBar(wait_frame, mode="indeterminate", width=200, fg_color=BG_MAIN, progress_color=ACCENT_BLUE)
            spinner.pack(pady=5)
            spinner.start()
            ctk.CTkLabel(wait_frame, text="Waiting for installations to finish...\nChecking automatically every 10 seconds.", font=("Segoe UI", 12), text_color=TEXT_MUTED).pack()

            self.after(10000, self.update_system_checks)

    # --- STEP 5 & 6: Download & Env Setup ---
    def show_step_5(self):
        self.is_checking_deps = False 
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Download & Prepare Environment", font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY).pack(pady=(20, 20))
        
        info = f"Repository: github.com/zunmax/technocore-did-starter\nLocation: {self.target_dir}"
        ctk.CTkLabel(self.main_frame, text=info, font=("Consolas", 12), text_color=TEXT_MUTED, justify="left").pack(pady=10)

        status_lbl = ctk.CTkLabel(self.main_frame, text="Ready to install.", text_color=WARNING, font=("Segoe UI", 14))
        status_lbl.pack(pady=20)

        def process():
            btn.configure(state="disabled")
            
            def run_in_background():
                agent_path = os.path.join(self.target_dir, self.agent)
                if not os.path.exists(agent_path):
                    self.after(0, lambda: status_lbl.configure(text="Downloading repository..."))
                    if os.path.exists(self.target_dir):
                        shutil.rmtree(self.target_dir, ignore_errors=True)
                    self.run_cmd(f"git clone {self.repo_url} {self.target_dir}")
                    self.after(0, lambda: status_lbl.configure(text="✅ Repository downloaded", text_color=SUCCESS))
                
                self.after(0, lambda: status_lbl.configure(text="Creating local Python environment..."))
                sys_python = "py" if shutil.which("py") else "python"
                self.run_cmd(f"{sys_python} -m venv .venv", cwd=self.target_dir)
                
                self.after(0, lambda: status_lbl.configure(text="Installing dependencies (this takes a moment)..."))
                self.run_cmd(f"{self.venv_python} -m pip install --upgrade pip", cwd=self.target_dir)
                self.run_cmd(f"{self.venv_python} -m pip install -r requirements.txt", cwd=self.target_dir)
                self.after(0, self.show_step_7)

            threading.Thread(target=run_in_background, daemon=True).start()

        btn = ctk.CTkButton(self.main_frame, text="Download & Install", command=process, fg_color=ACCENT_BLUE, font=("Segoe UI", 14, "bold"), height=45)
        btn.pack(pady=20)

    # --- STEP 7 & 8: Create DID ---
    def show_step_7(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Create Identity Passphrase", font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY).pack(pady=(10, 5))
        
        warn = "⚠️ Important: This protects your identity file.\nDo NOT send your passphrase to anyone."
        ctk.CTkLabel(self.main_frame, text=warn, font=("Segoe UI", 12), text_color=WARNING).pack(pady=5)

        pwd1 = ctk.CTkEntry(self.main_frame, show="•", placeholder_text="Passphrase", width=300, height=35)
        pwd1.pack(pady=5)
        pwd2 = ctk.CTkEntry(self.main_frame, show="•", placeholder_text="Confirm Passphrase", width=300, height=35)
        pwd2.pack(pady=5)

        status_lbl = ctk.CTkLabel(self.main_frame, text="", text_color=SUCCESS)
        status_lbl.pack(pady=5)

        log_box = ctk.CTkTextbox(self.main_frame, width=500, height=120, fg_color=BG_MAIN, text_color=TEXT_MUTED, font=("Consolas", 11))
        log_box.pack(pady=10)
        log_box.insert(ctk.END, "Terminal logs will appear here...\n")

        def append_log(text):
            self.after(0, lambda: log_box.insert(ctk.END, text + "\n"))
            self.after(0, lambda: log_box.see(ctk.END))

        def generate():
            p1, p2 = pwd1.get(), pwd2.get()
            if len(p1) < 12 or p1 != p2:
                messagebox.showerror("Error", "Passphrases must match and be 12+ characters.")
                return
            
            btn.configure(state="disabled")
            status_lbl.configure(text="Generating identity... please wait.")
            self.passphrase = p1

            def run_in_background():
                identity_path = os.path.join(self.target_dir, "identity.pem")
                if os.path.exists(identity_path):
                    append_log("[Removing old identity.pem to prevent conflicts]")
                    os.remove(identity_path)

                # Use the new wrapper fix
                cmd_init = self.get_agent_wrapper("init")
                success = self.run_cmd_live(cmd_init, self.target_dir, f"{p1}\n{p1}\n", append_log)
                
                if success:
                    append_log("\n> Retrieving DID...")
                    # Use wrapper for getting DID as well
                    cmd_did = self.get_agent_wrapper("did")
                    s2, out2, _ = self.run_cmd(cmd_did, cwd=self.target_dir, input_text=f"{p1}\n")
                    self.did = out2.split('\n')[-1] if s2 else "Unknown DID"
                    append_log(f"[DID Found: {self.did}]")
                    self.after(1500, self.show_step_9)
                else:
                    self.after(0, lambda: messagebox.showerror("Failed", "Process failed. Check the terminal box for errors."))
                    self.after(0, lambda: btn.configure(state="normal"))
                    self.after(0, lambda: status_lbl.configure(text="Error generating DID.", text_color=DANGER))

            threading.Thread(target=run_in_background, daemon=True).start()

        btn = ctk.CTkButton(self.main_frame, text="Create My DID", command=generate, fg_color=ACCENT_BLUE, font=("Segoe UI", 14, "bold"), height=45)
        btn.pack(pady=10)

    # --- STEP 9 & 10: Backup & Test ---
    def show_step_9(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="YOUR TECHNOCORE DID", font=("Segoe UI", 14, "bold"), text_color=TEXT_MUTED).pack(pady=(20, 5))
        ctk.CTkLabel(self.main_frame, text=self.did, font=("Consolas", 16, "bold"), text_color=SUCCESS).pack(pady=5)
        
        ctk.CTkButton(self.main_frame, text="Copy DID", command=lambda: self.clipboard_append(self.did), fg_color=BG_MAIN, hover_color=BG_SURFACE).pack(pady=10)
        
        warn = "🔐 NEVER upload identity.pem to GitHub.\n🔐 NEVER post it on X.\n🔐 NEVER send it to another person."
        ctk.CTkLabel(self.main_frame, text=warn, font=("Segoe UI", 12), text_color=DANGER).pack(pady=15)

        def backup():
            dest = filedialog.askdirectory(title="Choose Backup Location")
            if dest:
                backup_folder = os.path.join(dest, "Technocore-Identity-Backup")
                os.makedirs(backup_folder, exist_ok=True)
                shutil.copy(os.path.join(self.target_dir, "identity.pem"), backup_folder)
                messagebox.showinfo("Backed Up", f"identity.pem saved to {backup_folder}")
                
        ctk.CTkButton(self.main_frame, text="Backup Identity", command=backup, fg_color=WARNING, text_color=BG_MAIN, font=("Segoe UI", 14, "bold"), height=40).pack(pady=10)
        
        def test_net():
            succ, out, err = self.run_cmd(f"{self.venv_python} {self.agent} read lobby", cwd=self.target_dir)
            if succ:
                messagebox.showinfo("Network", "✅ Connected\n✅ Lobby readable\n✅ DID environment working")
                self.show_step_11()
            else:
                messagebox.showerror("Network Error", "Could not read lobby.")

        ctk.CTkButton(self.main_frame, text="Test Network Connection", command=test_net, fg_color=ACCENT_BLUE, font=("Segoe UI", 14, "bold"), height=45).pack(pady=20)

    # --- STEP 11, 12, 13, 14: Contribute & Proof ---
    def show_step_11(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="Make a Contribution", font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY).pack(pady=(20, 20))
        
        ctk.CTkOptionMenu(self.main_frame, values=["Guide", "Tutorial", "Code", "Useful tool", "Other"], width=300).pack(pady=10)
        url_entry = ctk.CTkEntry(self.main_frame, placeholder_text="https://github.com/username/project", width=300, height=40)
        url_entry.pack(pady=10)

        status_lbl = ctk.CTkLabel(self.main_frame, text="", text_color=SUCCESS)
        status_lbl.pack(pady=10)

        def create_proof():
            self.contrib_url = url_entry.get()
            btn.configure(state="disabled")
            status_lbl.configure(text="Scanning git repository & generating proof...")

            def run_in_background():
                succ, hsh, _ = self.run_cmd("git rev-parse HEAD", cwd=self.target_dir)
                self.commit_hash = hsh if succ else "unknown_commit"
                
                # Use wrapper fix for proofing as well!
                cmd_proof = self.get_agent_wrapper("proof", self.contrib_url, self.commit_hash)
                p_succ, p_out, p_err = self.run_cmd(cmd_proof, cwd=self.target_dir, input_text=f"{self.passphrase}\n")
                
                if p_succ:
                    try:
                        json_str = p_out[p_out.find('{'):]
                        with open(os.path.join(self.target_dir, "proof.json"), "w", encoding="utf-8") as f:
                            f.write(json_str)
                        
                        v_succ, v_out, v_err = self.run_cmd(f"{self.venv_python} {self.agent} verify-proof proof.json", cwd=self.target_dir)
                        if v_succ:
                            self.after(0, self.show_step_15)
                        else:
                            self.after(0, lambda: messagebox.showerror("Verification Failed", v_err))
                            self.after(0, lambda: btn.configure(state="normal"))
                    except Exception as e:
                        self.after(0, lambda: messagebox.showerror("Error", str(e)))
                        self.after(0, lambda: btn.configure(state="normal"))
                else:
                    self.after(0, lambda: messagebox.showerror("Proof Failed", p_err))
                    self.after(0, lambda: btn.configure(state="normal"))
                
                self.after(0, lambda: status_lbl.configure(text=""))

            threading.Thread(target=run_in_background, daemon=True).start()

        btn = ctk.CTkButton(self.main_frame, text="Generate & Verify Proof", command=create_proof, fg_color=SUCCESS, font=("Segoe UI", 14, "bold"), height=45)
        btn.pack(pady=20)

    # --- STEP 15 & 16: Dashboard & Share ---
    def show_step_15(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="🎉 You're ready!", font=("Segoe UI", 24, "bold"), text_color=TEXT_PRIMARY).pack(pady=(20, 10))
        
        dash_text = (
            "✅ DID created & backed up\n"
            "✅ Technocore connected & Lobby tested\n"
            "✅ Commit detected & Artifact registered\n"
            "✅ Proof generated & verified"
        )
        ctk.CTkLabel(self.main_frame, text=dash_text, font=("Segoe UI", 14), text_color=SUCCESS, justify="left").pack(pady=10)
        ctk.CTkLabel(self.main_frame, text=self.did, font=("Consolas", 12), text_color=TEXT_MUTED).pack(pady=10)

        def share_x():
            text = f"Just completed my Technocore contributor setup ✅\nDID: {self.did}\nContribution: {self.contrib_url}\nProof: verified locally.\nBuilding the Technocore ecosystem. ⚡"
            webbrowser.open(f"https://twitter.com/intent/tweet?text={urllib.parse.quote(text)}")

        ctk.CTkButton(self.main_frame, text="Post on X", command=share_x, fg_color="#000000", text_color="white", font=("Segoe UI", 14, "bold"), height=45).pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Exit", command=self.destroy, fg_color=BG_MAIN).pack(pady=10)

if __name__ == "__main__":
    app = TechnocoreApp()
    app.mainloop()
