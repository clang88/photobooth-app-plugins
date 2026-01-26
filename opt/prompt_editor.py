#!/usr/bin/env python3
"""
Lightweight HTTP server for editing photobooth prompts.
Usage: python prompt_editor.py [port]
Default port: 8080
"""

import http.server
import json
import os
import socketserver
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Get the project root directory (parent of opt/)
PROJECT_ROOT = Path(__file__).parent.parent
PROMPT_FILE = PROJECT_ROOT / "config" / "prompts" / "prompt.txt"
HISTORY_FILE = PROJECT_ROOT / "config" / "prompts" / "prompts_history.txt"

# Ensure directories exist
PROMPT_FILE.parent.mkdir(parents=True, exist_ok=True)

# HTML template with embedded JavaScript and CSS
HTML_TEMPLATE = open(Path(__file__).parent / "prompt_editor_html_template.html").read()


class PromptEditorHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the prompt editor."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/" or parsed_path.path == "/index.html":
            # Serve the main HTML page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
            
        elif parsed_path.path == "/api/prompts":
            # Return current prompt and history
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            current_prompt = ""
            if PROMPT_FILE.exists():
                current_prompt = PROMPT_FILE.read_text()
            
            history = []
            if HISTORY_FILE.exists():
                lines = HISTORY_FILE.read_text().strip().split("\n")
                for line in lines:
                    if line.strip():
                        parts = line.split("|||", 1)
                        if len(parts) == 2:
                            history.append({
                                "timestamp": parts[0].strip(),
                                "text": parts[1].strip()
                            })
                        else:
                            # Continuation of previous prompt
                            if history:
                                history[-1]["text"] += "\n" + line.strip()
            
            # Reverse to show newest first
            history.reverse()
            
            response = {
                "current": current_prompt,
                "history": history
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/api/update":
            # Read POST data
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                prompt = data.get("prompt", "").strip()
                
                if not prompt:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Empty prompt"}).encode())
                    return
                
                # Save to current prompt file
                PROMPT_FILE.write_text(prompt)
                
                # Append to history with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_entry = f"{timestamp} ||| {prompt}\n"
                
                with open(HISTORY_FILE, "a") as f:
                    f.write(history_entry)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                
                print(f"[{timestamp}] Prompt updated: {prompt[:50]}...")
                
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                print(f"Error: {e}")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8080):
    """Start the HTTP server."""
    with socketserver.TCPServer(("", port), PromptEditorHandler) as httpd:
        print(f"🚀 Prompt Editor Server running at http://localhost:{port}")
        print(f"📝 Prompt file: {PROMPT_FILE}")
        print(f"📚 History file: {HISTORY_FILE}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")


if __name__ == "__main__":
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port)
