import pulumi


class GeneralizedImage(pulumi.ComponentResource):
    def __init__(self, name: str, image_blob=None, opts=None):
        super().__init__('custom:resources:GeneralizedImage', name, opts=opts)
        self.name = name
        self.image_blob = image_blob
        # TODO
    def add_providers(providers: str[]):
        for p in providers:
            if p = "aws":
                if provider == "aws":
                    if "aws" not in self.instance:
                        # self.instance["aws"] = TODO
                else:
                    raise ValueError("Provider not implemented")






