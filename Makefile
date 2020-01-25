.PHONY: default
default: build

.PHONY: build
build:
	docker build --pull --no-cache --force-rm -t fingerprinter .

.PHONY: run-local
run-local:
	docker run  --mount 'src=$(PWD)/mnt,dst=/audio_fp/vol,type=bind' -it fingerprinter

.PHONY: run-bash
run-bash:
	docker run --mount 'src=$(PWD)/mnt,dst=/audio_fp/vol,type=bind' --entrypoint "/bin/bash" -it fingerprinter
