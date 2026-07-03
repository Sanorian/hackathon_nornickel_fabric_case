FROM ollama/ollama:latest
RUN ollama serve > /dev/null 2>&1 & \
    sleep 10 && \
    ollama pull nomic-embed-text
EXPOSE 11434
CMD ["serve"]