FROM python:3.11-slim

WORKDIR /app

# Copy requirements from parent directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from parent directory
COPY . .

# Expose port
EXPOSE 8006

# Set environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Run the MCP server using uvicorn for correct ASGI app loading
CMD ["uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "8006", "--reload", "--log-level", "debug"]
