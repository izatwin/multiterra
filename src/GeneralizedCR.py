import pulumi

class GeneralizedCR(pulumi.ComponentResource):
    def __init__(self, identifier: str, name: str, deps: List[GeneralizedCR], opts=None):
        super().__init__(identifier, name, opts=opts)
        self.identifier = identifier
        self.name = name
        self.__deps = deps
        self.__instance_matrix = dict()
        self.__providers = set()
        self.__regions = set()

    def get_instance(self, provider: str, region: str):
        return self.__instance_matrix[f"{provider}-{region}"]

    def set_regions(self, regions: Set[str]):
        self.__regions.update(regions)
        self.__populate_matrix()

    def set_providers(self, providers: Set[str]):
        self.__providers.update(providers)
        self.__populate_matrix()

    def __populate_matrix(self):
        # Update deps first
        for dep in self.__deps:
            dep.set_regions(self.__regions)
            dep.set_providers(self.__providers)
        for p in self.__providers:
            func_name = f"_create_{p}"
            create_func = getattr(self, func_name, None)
            if create_func is None or not callable(create_func):
                print(func_name)
                raise ValueError(f"Provider {p} not implemented on {type(self)}")
            for r in self.__regions:
                instance_id = f"{p}-{r}"
                if instance_id in self.__instance_matrix:
                    continue
                self.__instance_matrix[instance_id] = create_func(r)






