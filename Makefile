
voice_sample_test:
	@find output/voice -name "*" -type f -print0  | shuf -n1 -z | xargs -I {} sh -c 'basename "{}"; afplay "{}"'
