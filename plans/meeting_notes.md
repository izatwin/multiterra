# Meeting Notes

## March 25th

### Topics:

+ Is terraform a good starting point? Should we based this on [SST Serverless](https://sst.dev/) or [Pulumi](https://www.pulumi.com/) instead?

  Decision: Switch to using Pulumi.
  Reason: Seems to allow for additional logic for configuration with useful abstractions.

+ What is our MVP?

  Making a new Pulumi componenti in Python with opinionated decisions on resource creation. Supports 2-3 providers with a commonly defined interface.
  Resources can be switched by only changing one variable denoting the provider. MVP will include networking and virtual machines.
  Each resource type, we will have a new python class implementing the abstraction from every provider to our common interface definitions.

  - Extremely simple program that can create a VM in AWS and GCP

  Goal: One common definition for all clouds. Any one definition can deploy to any supported cloud.

+ Possible Project Renaming? maybe to Simpleform

+ What is the bare minimum needed for each cloud provider for the MVP?

  - Name of resource
  - be able to choose between a couple different 'tiers' like low mid high which we would map to different ram and cpu configs
  - networking options
  - Custom images

+ How to divide work?

+ Next Meeting Time?

  March 28th

## March 28th

Agenda: Create simple main.py and VM resource class for AWS EC2 VMs.







