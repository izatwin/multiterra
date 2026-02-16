# multiterra

An opinionated wrapper for terraform to generate configs for various providers using a single spec file.

Providers to start out supporting: AWS, GCP

Current workflow: run 'python teracloud.py' and see the generated .tf files

Future work: complete the boilerplate .tf files.
run terraform validate to check validity of generated terraform.