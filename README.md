# Technocore Contributor Wizard ⚡

A frictionless, secure desktop application designed to help users onboard and contribute to the Technocore ecosystem without needing to touch the command line.

## 🎯 What This Tool Does
The Technocore CLI is powerful, but setting up Python environments, handling Git commands, and managing cryptographic keys can be overwhelming for beginners. 

This UI wrapper automates the entire process from A to Z on your local Windows machine:
* **Zero-Setup Environment:** Automatically detects Python/Git, downloads the Technocore starter repository, and builds the local virtual environment.
* **Secure Local Identity:** Injects passphrases securely via background threads. Your `identity.pem` private key is generated locally and *never* leaves your machine.
* **Frictionless Proofs:** Automatically detects your Git commit hashes and generates valid `proof.json` files for your contributions.
* **No Freezes:** Runs all heavy CLI operations in background threads with live terminal logging to keep the UI smooth and responsive.

## 🚀 How to Use (For Beginners)

You do not need to install Python libraries to run this app.
1. Go to the **[Releases](../../releases)** page on the right side of this repository.
2. Download the latest `technocore_wizard.exe` file.
3. Double-click the file to launch the setup wizard.
4. Follow the on-screen instructions to create your DID and submit your contribution!
