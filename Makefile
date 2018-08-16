IMAGE_NAME ?= "quay.io/influxdb/litmus"
IMG_TAG ?= "dirty"
DOCKER ?= docker

.PHONY: image/build
image/build:
	$(DOCKER) build -f Dockerfile -t $(IMAGE_NAME):$(IMG_TAG) .

.PHONY: image/publish
image/publish:
	$(DOCKER) push $(IMAGE_NAME):$(IMG_TAG)

.PHONY: image/publish-latest
image/publish-latest:
	$(DOCKER) tag $(IMAGE_NAME):$(IMG_TAG) $(IMAGE_NAME):latest
	$(DOCKER) push $(IMAGE_NAME):latest
