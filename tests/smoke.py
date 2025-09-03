import os
os.system("python -m gmcp.main stdio & sleep 2; pkill -f gmcp.main || true")
print("OK: started and stopped stdio server")
os.environ["GMCP_HTTP"] = "1"
os.system("python -m gmcp.main http & sleep 2; pkill -f gmcp.main || true")
print("OK: started and stopped HTTP server")