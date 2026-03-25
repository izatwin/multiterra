# Meeting Notes

## March 25th

Topics:

+ Is terraform a good starting point? Should we based this on [SST Serverless](https://sst.dev/) or [Pulumi](https://www.pulumi.com/) instead?

  Decision: Switch to using Pulumi.
  Reason: Seems to allow for additional logic for configuration with useful abstractions.

+ What is our MVP?

  Making a new Pulumi component with opinionated decisions on resource creation. Supports 2-3 providers with a commonly defined interface.
  Resources can be switched by only changing one variable denoting the provider.

  Goal: One common definition for all clouds. Any one definition can deploy to any supported cloud.

+ Possible Project Renaming? maybe to Simpleform

+ What is the bare minimum needed for each cloud provider for the MVP?
### MVP
+ Extremely simple program that can create a VM in AWS and GCP
+ be able to choose between a couple different 'tiers' like low mid high which we would map to different ram and cpu configs
+ networking options
+ 



+ How to divide work?

+ Next Meeting Time?





