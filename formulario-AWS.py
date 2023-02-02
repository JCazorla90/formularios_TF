import os

file_path = input("Ingresa la ruta del archivo: ")

region = input("Ingresa la región deseada: ")
ami = input("Ingresa la AMI: ")
vpc_id = input("Ingresa el ID del VPC: ")
subnet_id = input("Ingresa el ID de la subred: ")
instance_type = input("Ingresa el tipo de instancia: ")
num_instances = int(input("Ingresa el número de máquinas: "))
persistent = input("La infraestructura es persistente (sí o no): ").lower() == "sí"

instance_count = "count = {}".format(num_instances) if persistent else ""

template = f"""provider "aws" {{
region = "{region}"
}}

resource "aws_vpc" "example" {{
id = "{vpc_id}"
}}

resource "aws_subnet" "example" {{
vpc_id = aws_vpc.example.id
cidr_block = "{subnet_id}"
}}

resource "aws_instance" "example" {{
{instance_count}
ami = "{ami}"
instance_type = "{instance_type}"
subnet_id = aws_subnet.example.id
}}

resource "aws_s3_bucket" "example" {{
bucket = "terraform-states-{vpc_id}"
}}

terraform {
backend "s3" {{
bucket = aws_s3_bucket.example.bucket
key = "terraform.tfstate"
region = "{region}"
}}
}"""

with open(file_path, "w") as f:
f.write(template)

print("Archivo Terraform creado exitosamente en:", file_path)