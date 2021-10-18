## Steps

### Download Stack Overflow data

- Go to https://archive.org/details/stackexchange

There are a lot of archives available for download.

For example, the DevOps archive can be found at:
https://archive.org/download/stackexchange/devops.stackexchange.com.7z

### Extract the data

- Make a folder inside the `data` folder (example: `devops`)
- Extract the downloaded archive somewhere
- Copy the file `Posts.xml` from the extracted archive to the created folder

### Build the Docker image

`./scripts/build-base.sh`

### Spawn the corpus files

`./scripts/build-corpus.sh`

### Try to classify the data

`./scripts/classify-intents.sh devops`

### Try to analyze a conversation

`./scripts/analyze-conversation.sh devops conversation2.tsv`
