FROM ollama/ollama:latest
RUN ollama serve > /dev/null 2>&1 & \
    sleep 10 && \
    ollama pull gemma4:12b
RUN RUN ollama serve > /dev/null 2>&1 & \
    sleep 10 && \
    ollama pull embeddinggemma
EXPOSE 11434
CMD ["serve"]