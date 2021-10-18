docker run \
-it --rm \
-v $(pwd)/data/${1}:/opt/data \
-v $(pwd)/corpus/${1}:/opt/corpus \
-v $(pwd)/samples:/opt/samples \
-v $(pwd)/src:/opt/src \
nlp/sample2 \
bash -c "python3 analyze-conversation.py ${2}"
